import datetime
import locale
import os
import re
import sys
import webbrowser
from enum import IntEnum, unique
from pathlib import Path
from urllib.parse import urlparse

import click
import pkg_resources

from .calendar import HTMLCalendar
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


@click.command(context_settings={"show_default": True})
@click.option(
    "--width",
    type=click.IntRange(1, 12, clamp=True),
    default=3,
    help="Width of columns.",
)
@click.option("--output", "-o", default="calendar.html", help="Output HTML filename.")
@click.option(
    "--css",
    default=None,
    help="Output css filename. (relative from output directory)",
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
@click.option("--encoding", default="utf-8", help="Character encoding for HTML.")
@click.option("--locale", "locale_", default=None, help="Locale eg. en_US.UTF-8.")
@click.option(
    "--country",
    "-c",
    default=None,
    help="Country code for holidays. eg. US (default is same as locale)",
)
@click.option("--subdiv", default=None, help="Specify subdivision.")
@click.option("--financial", default=None, help="Use financial holiday.")
@click.option("--force", "-f", is_flag=True, help="Force overwrite css file.")
@click.option("--no-browser", is_flag=True, help="Do not open browser.")
@click.option("--verbose", "-v", is_flag=True, help="Show information.")
@click.argument(
    "year",
    type=click.IntRange(1949, 3000),
    default=datetime.date.today().year,
    required=False,
)
@click.argument(
    "first-weekday",
    type=click.Choice(list(Weekday.__members__)),
    default="mon",
    required=False,
)
@click.argument("start-month", type=click.IntRange(1, 12), default=1, required=False)
def main(
    width,
    country,
    subdiv,
    financial,
    output,
    css,
    css_href,
    style,
    encoding,
    locale_,
    first_weekday,
    start_month,
    force,
    no_browser,
    verbose,
    year,
):
    lc_time = (
        locale_
        or os.getenv("LC_ALL")
        or os.getenv("LC_TIME")
        or os.getenv("LANG")
        or locale.getdefaultlocale()[0]
        or "C"
    )

    lc_time_orig = lc_time
    if "." not in lc_time:
        lc_time = lc_time + ".UTF-8"

    try:
        locale.setlocale(locale.LC_TIME, lc_time)
    except locale.Error as exc:
        print(f"Bad locale {lc_time_orig}: {exc}", file=sys.stderr)
        print("Please check available locale on your system.", file=sys.stderr)
        sys.exit(1)

    first_weekday = Weekday[first_weekday]

    if financial is None and country is None:
        match = re.match("^[a-z]{2}_([a-z]{2})", lc_time, re.I)
        if match:
            country = match.group(1)
            print(f"Holiday region is {country}.", file=sys.stderr)
        else:
            print(
                f"warning: Can not detect coutry from locale {lc_time}",
                file=sys.stderr,
            )
            print(
                "Plase use --country option.",
                file=sys.stderr,
            )
            sys.exit(1)

    # when output filename is calendar.html.
    #   --css      --css_href
    #   None       None         write calendar.css
    #   None       ./my.css     do not write css and include ./my.css in HTML
    #   ''         None         do not write css and not include css in HTML
    #   ''         ./my.css     do not write css and include ./my.css in HTML
    #   style.css  None         write style.css and include ./style.css in HTML
    #   style.css  ./foo.css    write style.css and include ./foo.css in HTML

    if css_href is not None and urlparse(css_href).scheme == "":
        if Path(css_href).is_absolute():
            print("Can not use absolute path for css-href option.", file=sys.stderr)
            sys.exit(1)

    css_file = None
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

    if verbose:
        print(f"year: {year}")
        print(f"locale: {lc_time}")
        print(f"financial: {financial}")
        print(f"holiday region: {country}")
        print(f"subdiv: {subdiv}")
        print(f"output: {output}")
        print(f"style: {style}")
        print(f"css_file: {css_file}")
        print(f"css_href: {css_href}")
        print(f"encoding: {encoding}")

    # write css file
    if css_file is not None:
        if force or not os.path.exists(css_file):
            Path(css_file).parent.mkdir(parents=True, exist_ok=True)
            with open(css_file, "wb") as out:
                try:
                    with get_css_stream(style or "default") as stream:
                        template = stream.read()
                except ValueError as exc:
                    print(str(exc), file=sys.stderr)
                    sys.exit(1)
                out.write(template)
        else:
            print(
                f"{css_file} exists. add --force option to overwrite css.",
                file=sys.stderr,
            )

    # write html file
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with open(output, "wb") as fh:
        cal = HTMLCalendar(
            firstweekday=first_weekday,
            startmonth=start_month,
            country=country,
            financial=financial,
            subdiv=subdiv,
        )
        fh.write(cal.formatyearpage(year, width=width, css=css_href, encoding=encoding))

    if not no_browser:
        webbrowser.open(output)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
