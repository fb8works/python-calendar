from python_calendar.calendar import HTMLCalendar
from python_calendar.util import dot_path


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
