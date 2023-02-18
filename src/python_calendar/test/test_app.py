import datetime

from python_calendar.calendar import HTMLCalendar
from python_calendar.util import dot_path

from .holidays import Holidays


def test_app():
    css_in = "test-calendar.css"
    css = dot_path(css_in)
    assert css == "./" + css_in

    cal = HTMLCalendar(
        firstweekday=0, startmonth=4, country="US", financial=False, subdiv=None
    )
    html = cal.formatyearpage(2023, width=3, css=css, encoding="utf-8")
    html = html.decode("utf-8")

    assert 'encoding="utf-8"' in html
    assert ">2023<" in html
    assert 'href="' + css + '"' in html
    assert "Martin Luther King Jr. Day" in html


def test_normalize_holiday_name():
    dt = datetime.date(1999, 10, 10)
    instance = Holidays()
    name1 = instance.get_holiday_name(dt)
    name2 = instance.normalize_name(name1)
    assert name1 == "体育の日"
    assert name2 == "スポーツの日"
