import datetime
import locale
import os
import re
import sys
import webbrowser
from pathlib import Path

import click
import pkg_resources

from .calendar import HTMLCalendar
from .util import dot_path


@click.command(context_settings={"show_default": True})
@click.option("--year", default=datetime.date.today().year, help="Target year")
@click.option(
    "--width",
    type=click.IntRange(1, 12, clamp=True),
    default=3,
    help="Width of columns",
)
@click.option("--output", default="calendar.html", help="Output HTML filename")
@click.option(
    "--css",
    default=None,
    help="Output css filename/URL (relative from output filename)",
)
@click.option(
    "--style",
    type=click.Choice(["default", "simple"], case_sensitive=False),
    default="default",
    help="CSS template name",
)
@click.option("--encoding", default="utf-8", help="output character encoding")
@click.option("--locale", "locale_", default=None, help="Locale eg. en_US.UTF-8")
@click.option(
    "--country",
    default=None,
    help="Country code for holidays. eg. en (default is same as locale)",
)
@click.option("--subdiv", default=None, help="Subdivision")
@click.option(
    "--financial", is_flag=True, help="Use financial holiday (with --country=NYSE)"
)
@click.option(
    "--first-weekday",
    type=click.IntRange(0, 6, clamp=True),
    default=0,
    help="First weekday (0:mon - 6:sun)",
)
@click.option(
    "--start-month",
    type=click.IntRange(1, 12, clamp=True),
    default=4,
    help="Start month",
)
@click.option("--force", is_flag=True, help="Force overwrite css file")
@click.option("--no-browser", is_flag=True, help="Do not open browser")
@click.option("--verbose", is_flag=True, help="Show information")
def main(
    year,
    width,
    country,
    subdiv,
    financial,
    output,
    css,
    style,
    encoding,
    locale_,
    first_weekday,
    start_month,
    force,
    no_browser,
    verbose,
):
    lc_time = (
        locale_
        or os.getenv("LC_ALL")
        or os.getenv("LC_TIME")
        or os.getenv("LANG")
        or locale.getdefaultlocale()[0]
        or "C"
    )

    if "." not in lc_time:
        lc_time += ".UTF-8"

    try:
        locale.setlocale(locale.LC_TIME, lc_time)
    except locale.Error:
        print(f"Bad locale {lc_time}", file=sys.stderr)
        print("Please available locale in your system. eg. locale -a.", file=sys.stderr)
        sys.exit(1)

    if country is None:
        if financial:
            country = "NYSE"
        else:
            match = re.match("^[a-z]{2}_([a-z]{2})", lc_time, re.I)
            if match:
                country = match.group(1)
                print(f"Holiday region: {country}.")
            else:
                print(
                    f"Bad locale {lc_time}. please use --country option.",
                    file=sys.stderr,
                )
                sys.exit(1)

    css_presets = {
        "default": "styles/calendar.css",
        "simple": "styles/calendar-simple.css",
    }
    css_template = css_presets.get(style or "default")
    if css_template is None:
        print(f"No such style {style}", file=sys.stderr)
        sys.exit(1)

    if css is None:
        css = Path(output).with_suffix(".css").name

    if css_template:
        if force or not os.path.exists(css):
            stream = pkg_resources.resource_stream("python_calendar", css_template)
            with open(css, "wb") as out:
                out.write(stream.read())
            stream.close()

    if verbose:
        print(f"year: {year}")
        print(f"locale: {lc_time}")
        print(f"country: {country}")
        print(f"subdiv: {subdiv}")
        print(f"financial: {financial}")
        print(f"output: {output}")
        print(f"css: {css}")
        print(f"encoding: {encoding}")

    with open(output, "wb") as fh:
        cal = HTMLCalendar(
            firstweekday=first_weekday,
            startmonth=start_month,
            country=country,
            financial=financial,
            subdiv=subdiv,
        )
        fh.write(
            cal.formatyearpage(year, width=width, css=dot_path(css), encoding=encoding)
        )

    if not no_browser:
        webbrowser.open(output)


# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    main()
