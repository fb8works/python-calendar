import datetime
import locale
import os
import re
import shutil
import subprocess
import sys
import webbrowser
from contextlib import contextmanager
from enum import IntEnum, unique
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import MutableSequence
from urllib.parse import urlparse

import click
import pkg_resources
from inscriptis import get_text

from .calendar import HTMLCalendar
from .locale_win import normalize_locale_win
from .util import dot_path


@unique
class Weekday(IntEnum):
    mon = 0
    tue = 1
    wed = 2
    thu = 3
    fri = 4
    sat = 5
    sun = 6


class YearOrMonth(click.ParamType):
    def convert(self, value, param, ctx):
        if value == ".":
            value = "0"
        try:
            int_value = int(value)
        except ValueError:
            self.fail(f"{value!r} is not a valid integer.", param, ctx)
        if not (0 <= int_value <= 12 or 1900 <= int_value <= 3000):
            self.fail(f"{int_value} is not a valid year or month.", param, ctx)
        return super().convert(value, param, ctx)


def get_year_month(args, today, maybe_anual):
    if not (isinstance(args, tuple) or isinstance(args, MutableSequence)):
        raise ValueError()

    if len(args) < 2:
        args = (list(args) + [None, None])[:2]

    year = None
    month = None

    if args[0] is not None and re.match("^1?[1-9]$", args[0]):
        month, year = args
    else:
        year, month = args

    if year is None and month is None:
        if maybe_anual:
            year = "0"
        else:
            year = "0"
            month = "0"

    if year in ("0", "."):
        year = today.year
    else:
        if year is not None:
            year = int(year)

    if month in ("0", "."):
        month = today.month
    else:
        if month is not None:
            month = int(month)

    return year, month


def get_css_stream(style):
    css_presets = {
        "default": "styles/calendar.css",
        "simple": "styles/calendar-simple.css",
    }
    css_template = css_presets.get(style or "default")
    if css_template is None:
        raise ValueError(f"No such style {style}")
    stream = pkg_resources.resource_stream("python_calendar", css_template)
    return stream


@contextmanager
def open_for_write_binary(filename):
    if filename == "-":
        yield sys.stdout.buffer
    else:
        folder = Path(filename).parent
        folder.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(dir=folder, delete=False, mode="w+b") as tmp:
            yield tmp
            Path(tmp.name).rename(filename)


@click.command(context_settings={"show_default": True})
@click.option("--text", "-t", "text_mode", is_flag=True, help="Text mode")
@click.option("--html", "-H", "html_mode", is_flag=True, help="HTML mode")
@click.option(
    "--width",
    "-w",
    type=click.IntRange(1, 12, clamp=True),
    default=None,
    help="Width of columns.",
)
@click.option(
    "--start-month", "-m", type=click.IntRange(1, 12), default=None, help="Start month."
)
@click.option(
    "--first-weekday",
    "-d",
    type=click.Choice(list(Weekday.__members__)),
    default="sun",
    help="First weekday.",
)
@click.option("--output", "-o", default=None, help="Output HTML filename.")
@click.option("--holidays", "-h", is_flag=True, help="Include holiday list.")
@click.option("--list-holidays", "-l", is_flag=True, help="List holidays.")
@click.option(
    "--css",
    "-c",
    default=None,
    help="Output css filename. (relative from output directory)",
)
@click.option(
    "--use-external-css",
    "-e",
    is_flag=True,
    help="Use external css file.",
)
@click.option(
    "--css-href",
    default=None,
    help="CSS location or URL.",
)
@click.option(
    "--style",
    "-s",
    type=click.Choice(["default", "simple"], case_sensitive=False),
    default="default",
    help="CSS template name.",
)
@click.option("--encoding", default=None, help="Character encoding for HTML.")
@click.option("--locale", "locale_", default=None, help="Locale eg. en_US.UTF-8.")
@click.option(
    "--country",
    "-C",
    default=None,
    help="Country code for holidays. eg. US (default is same as locale)",
)
@click.option("--subdiv", default=None, help="Specify subdivision.")
@click.option("--financial", default=None, help="Use financial holiday.")
@click.option("--force", "-f", is_flag=True, help="Force overwrite css file.")
@click.option("--quiet", "-q", is_flag=True, help="Quiet mode.")
@click.option(
    "--no-browser", "-n", is_flag=True, default=None, help="Do not open browser."
)
@click.option(
    "--color", "-c", is_flag=True, default=None, help="color mode (text mode)."
)
@click.option("--verbose", "-v", is_flag=True, help="Show information.")
@click.argument(
    "args",
    # type=click.IntRange(1949, 3000),
    type=YearOrMonth(),
    nargs=-1,
    required=False,
)
def main(
    text_mode,
    html_mode,
    width,
    start_month,
    first_weekday,
    country,
    subdiv,
    financial,
    output,
    holidays,
    list_holidays,
    css,
    use_external_css,
    css_href,
    style,
    encoding,
    locale_,
    force,
    no_browser,
    color,
    verbose,
    quiet,
    args,
):
    def print_error(message):
        if not quiet:
            print(message, file=sys.stderr)

    today = datetime.date.today()

    if len(args) > 2:
        print_error("Usage: pycal [OPTIONS] [YEAR] [MONTH]")
        sys.exit(1)

    year, month = get_year_month(args, today, maybe_anual=(width or start_month))

    if width is None:
        width = 3

    if start_month is None:
        start_month = 1

    if list_holidays:
        holidays = True

    if css_href:
        use_external_css = True

    if not html_mode and not text_mode:
        if (
            css_href
            or css
            or use_external_css
            or (
                output is not None
                and re.match(r"\.(html|htm|xml)", str(Path(output).suffix), re.I)
            )
        ):
            text_mode = False
        else:
            text_mode = True
    html_mode = not text_mode

    if html_mode:
        if output is None:
            if sys.stdout.isatty():
                # output = "calendar.html"
                if no_browser:
                    output = "-"
                else:
                    output_dir = Path.home().joinpath(".cache", "pycal")
                    output_dir.mkdir(parents=True, exist_ok=True)
                    output = str(output_dir.joinpath("calendar.html"))
                    if use_external_css:
                        print_error(
                            "warning: Can not use --use-external-css option without --output option."
                        )
                        use_external_css = False
            else:
                output = "-"
                if use_external_css:
                    print_error(
                        "warning: Can not use --use-external-css option when output is not a file."
                    )
                    use_external_css = False
        else:
            no_browser = True
    else:
        if output is None:
            output = "-"

    if output == "-":
        no_browser = True

    if color is None:
        color = sys.stdout.isatty()
    else:
        if color and text_mode is None:
            text_mode = True

    default_locale_candidates = (
        locale_,
        os.getenv("LC_ALL"),
        os.getenv("LC_TIME"),
        os.getenv("LANG"),
        ".".join(locale.getlocale()),  # Windows: Japanese_Japan.932
    )
    default_locale_candidates = [l for l in default_locale_candidates if l is not None]
    lc_time = next((l for l in default_locale_candidates if l is not None))
    lc_time_orig = lc_time

    locale_types = [
        "LC_COLLATE",
        "LC_CTYPE",
        "LC_MESSAGES",
        "LC_MONETARY",
        "LC_NUMERIC",
        "LC_TIME",
    ]
    locale_save = {}

    for name in locale_types:
        try:
            value = getattr(locale, name)
        except AttributeError:
            pass
        else:
            locale_save[name] = locale.getlocale(value)
    try:
        try:
            locale.setlocale(locale.LC_ALL, lc_time.split(".")[0])
        except locale.Error as exc:
            # setlocale(locale.LC_ALL, "en_US") -> unsupported locale setting
            pass
        default_encoding = locale.nl_langinfo(locale.CODESET)
    finally:
        locale.setlocale(locale.LC_ALL, "")
        for name in locale_save:
            locale.setlocale(getattr(locale, name), locale_save[name])

    if encoding is None:
        if "." in lc_time:
            encoding = lc_time.split(".")[1]
        else:
            temp = next((l for l in default_locale_candidates if "." in l), None)
            if temp:
                encoding = temp.split(".")[1]
            else:
                encoding = default_encoding

    try:
        try_lc_time = lc_time.split(".")[0] + "." + default_encoding
        locale.setlocale(locale.LC_TIME, try_lc_time)
        lc_time = try_lc_time
    except locale.Error as exc:
        try:
            locale.setlocale(locale.LC_TIME, lc_time)
        except:
            print_error(f"Bad locale {lc_time_orig}: {exc}")
            print_error("Please check available locale on your system.")
            sys.exit(1)
    finally:
        for name in locale_types:
            locale.setlocale(getattr(locale, name), locale_save[name])

    norm_lc = normalize_locale_win(lc_time)

    # Detect country from locale string
    if financial is None and country is None:
        match = re.match("^[a-z]{2}_([a-z]{2})", norm_lc, re.I)
        if match:
            country = match.group(1)
            if not quiet:
                print_error(f"Holiday region is {country}.")
        else:
            print_error(f"warning: Can not detect coutry from locale {lc_time}")
            print_error("Plase use --country option.")
            sys.exit(1)

    # when output filename is calendar.html.
    #   --css      --css_href
    #   None       None         write calendar.css
    #   None       ./my.css     do not write css and include ./my.css in HTML
    #   ""         None         do not write css and not include css in HTML
    #   ""         ./my.css     do not write css and include ./my.css in HTML
    #   style.css  None         write style.css and include ./style.css in HTML
    #   style.css  ./foo.css    write style.css and include ./foo.css in HTML

    if not use_external_css:
        if css_href:
            print_error("warning: --css_href option ignored.")
            css_href = None
    else:
        if css_href is not None:
            if text_mode:
                print_error("Can not use both --css_href and --text.")
                sys.exit(1)
            if urlparse(css_href).scheme == "":
                if Path(css_href).is_absolute():
                    print_error("Can not use absolute path for css-href option.")
                    sys.exit(1)

    css_file = None
    if html_mode:
        if use_external_css:
            if css is None:
                if css_href is None:
                    css_file = str(Path(output).with_suffix(".css"))
                    css_href = css
            else:
                if len(css.strip()) == 0:
                    if css_href is None:
                        css_href = ""  # Do not use css
                else:
                    css = Path(css)
                    if css.is_absolute():
                        css_file = str(css)
                    else:
                        css_file = Path(output).parent.joinpath(css)

            if css_href == "":
                css_href = None  # Do not add link tag for stylesheet
            else:
                if css_href is None and css_file is not None:
                    css_href = os.path.relpath(css_file, Path(output).parent)
                css_href = dot_path(css_href)

    start_month = month if month else start_month
    num_month = 12 if month is None else 1
    width = width if month is None else 1

    elinks = shutil.which("elinks")
    w3m = shutil.which("w3m")

    if verbose:
        print_error(f"text: {text_mode}")
        print_error(f"year: {year}")
        print_error(f"month: {month}")
        print_error(f"width: {width}")
        print_error(f"start_month: {start_month}")
        print_error(f"locale: {lc_time}")
        print_error(f"financial: {financial}")
        print_error(f"holiday region: {country}")
        print_error(f"subdiv: {subdiv}")
        print_error(f"output: {output}")
        print_error(f"style: {style}")
        print_error(f"css_file: {css_file}")
        print_error(f"css_href: {css_href}")
        print_error(f"use_external_css: {use_external_css}")
        print_error(f"encoding: {encoding}")
        print_error(f"default_encoding: {default_encoding}")
        print_error(f"color: {color}")
        print_error(f"elinks: {elinks}")
        print_error(f"w3m: {w3m}")

    # read or write css file
    css_content = None

    if not use_external_css:
        stream = None
        if css_file:
            try:
                stream = open(css_file, "r")
            except FileNotFoundError:
                print_error(f"No such CSS file: {css_file}")
                sys.exit(1)
            css_content = stream.read()
        else:
            try:
                stream = get_css_stream(style or "default")
            except ValueError as exc:
                print_error(str(exc))
                sys.exit(1)
            css_content = stream.read().decode("utf-8")
    else:
        if css_file is not None:
            if force or not os.path.exists(css_file):
                Path(css_file).parent.mkdir(parents=True, exist_ok=True)
                with open(css_file, "wb") as out:
                    try:
                        with get_css_stream(style or "default") as stream:
                            template = stream.read()
                    except ValueError as exc:
                        print_error(str(exc))
                        sys.exit(1)
                    out.write(template)
            else:
                print_error(f"{css_file} exists. add --force option to overwrite css.")

    visible_holiday = False
    visible_today = False
    inline_style = False

    if text_mode:
        if color and elinks:
            inline_style = True
        else:
            visible_holiday = True
            visible_today = True

    cal = HTMLCalendar(
        firstweekday=Weekday[first_weekday],
        locale=lc_time,
        startmonth=start_month,
        country=country,
        financial=financial,
        subdiv=subdiv,
        num_month=num_month,
        visible_holiday=visible_holiday,
        visible_today=visible_today,
        inline_style=inline_style,
        today=today,
    )
    formatyearpage = lambda: cal.formatyearpage(
        year,
        width=width,
        css=css_href,
        css_content=css_content,
        encoding=encoding,
        holidays=holidays,
        calendar=(not list_holidays),
    )
    try:
        content = formatyearpage()
    except NotImplementedError:
        if month:
            print_error("Can not create calendar for year {year}/{month}.")
        else:
            print_error("Can not create calendar for year {year}.")
        sys.exit(1)

    if text_mode:
        if elinks or w3m:
            if elinks:
                args = [elinks, "-dump", "-dump-color-mode", "1"]
            else:
                print_error("warning: elinks is not installed.")
                args = ["w3m", "-T", "text/html", "-dump", "-O", "utf-8"]
            proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            content = proc.communicate(content)[0].decode("utf-8")
            content = (
                "\n".join([l for l in content.split("\n") if l != ""]).encode(encoding)
                + b"\n"
            )
        else:
            print_error("warning: elinks or w3m is not installed.")
            content = get_text(content.decode(encoding)).encode(encoding)

    # write html file
    if output is not None:
        with open_for_write_binary(output) as fh:
            fh.write(content)
        if not quiet and no_browser and output != "-":
            print_error(f"Wrote {output}")

    if not text_mode and not no_browser:
        webbrowser.open(output)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
