import calendar
import datetime
import html

import holidays


class HTMLCalendar(calendar.LocaleHTMLCalendar):
    """
    This calendar returns complete HTML pages.
    """

    cssclass_noday = "day noday"
    cssclasses = [
        "day mon",
        "day tue",
        "day wed",
        "day thu",
        "day fri",
        "day sat",
        "day sun",
    ]
    cssclasses_weekday_head = [
        "wd mon",
        "wd tue",
        "wd wed",
        "wd thu",
        "wd fri",
        "wd sat",
        "wd sun",
    ]

    def __init__(
        self,
        firstweekday=0,
        locale=None,
        startmonth=1,
        country=None,
        financial=None,
        subdiv=None,
        num_month=12,
        visible_holiday=False,
        visible_today=False,
        inline_style=False,
        today=None,
    ):
        super().__init__(firstweekday, locale=locale)
        self.cur_year = None
        self.cur_month = None
        self.startmonth = startmonth
        self.num_month = num_month
        self.visible_holiday = visible_holiday
        self.visible_today = visible_today
        self.inline_style = inline_style
        self.today = today or datetime.date.today()
        if financial:
            self.holidays = holidays.financial_holidays(financial)
        else:
            self.holidays = holidays.country_holidays(country, subdiv=subdiv)

    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            # day outside month
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            this_date = datetime.date(self.cur_year, self.cur_month, day)
            holiday_name = self.holidays.get(this_date)
            css = self.cssclasses[weekday]
            day = str(day)
            styles = {}

            if holiday_name:
                if self.visible_holiday:
                    day = f"({day})"
                if self.inline_style:
                    styles["color"] = "red"

            if this_date == self.today:
                if self.visible_today:
                    day = f"[{day}]"
                if self.inline_style:
                    styles["background"] = "white"
                    styles.setdefault("color", "black")

            style = "; ".join([f"{k}: {v}" for k, v in styles.items()])
            day = f'<span style="{style}">{day}</span>'

            if holiday_name:
                styles["color"] = "red"
                css += " holiday"
                name = html.escape(holiday_name, quote=True)
                return '<td class="%s" title="%s"><div>%s</div></td>' % (css, name, day)
            else:
                return '<td class="%s">%s</td>' % (css, day)

    def formatweek(self, theweek):
        """
        Return a complete week as a table row.
        """
        s = "".join(self.formatday(d, wd) for (d, wd) in theweek)
        return '<tr class="days">%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table class="%s">' % (self.cssclass_month))
        a("\n")
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a("\n")
        a(self.formatweekheader())
        a("\n")

        # make noday cells (7days * 6week - {days in month})
        arr = self.monthdays2calendar(theyear, themonth)
        arr = arr + [[(0, 0)] * 7] * (6 - len(arr))

        for week in arr:
            a(self.formatweek(week))
            a("\n")
        a("</table>")
        a("\n")
        return "".join(v)

    def itermonthdates_just_month(self, year, month):
        d = datetime.date(year, month, 1)
        m = month + 1
        y = year + m // 12
        m = (month % 12) + 1
        next_month_day = datetime.date(y, m, 1)
        while d < next_month_day:
            yield d
            d += datetime.timedelta(days=1)

    def get_holiday_list(self, theyear):
        v = []
        for i in range(self.startmonth, self.startmonth + self.num_month):
            m = ((i - 1) % 12) + 1
            for d in self.itermonthdates_just_month(theyear, m):
                name = self.holidays.get(d)
                if name:
                    v.append((d, name))
        return v

    def formatholidays(self, theyear):
        v = []
        a = v.append
        a('<table class="%s">\n' % self.cssclass_year)
        for d, name in self.get_holiday_list(theyear):
            a("<tr><td>%s</td><td>%s</td></tr>" % (d, name))
        a("</table>\n")
        return "".join(v)

    def formatyear(self, theyear, width=3):
        """
        Return a formatted year as a table of tables.
        supports startmonth parameter.
        """
        v = []
        a = v.append
        width = max(width, 1)
        a('<table class="%s">' % self.cssclass_year)
        a("\n\n")
        a(
            '<tr><th colspan="%d" class="%s">%s</th></tr>'
            % (width + width - 1, self.cssclass_year_head, theyear)
        )

        for i in range(self.startmonth, self.startmonth + self.num_month, width):
            # months in this row
            a("\n")
            months = [((x - 1) % 12) + 1 for x in range(i, i + width)]
            a('<tr class="months-row">')
            for m in months:
                y = theyear + 1 if m < self.startmonth else theyear
                # save current year and date for test holiday
                self.cur_year = y
                self.cur_month = m
                a("\n\n")
                a('<td class="month">')
                a(self.formatmonth(y, m, withyear=False))
                a("</td>")
                # vertical space between month
                # NOTE: 単に <td></td> とすると excel に貼り付けたときに結合セルになってしまうので同じ個数の空セルで埋める。
                a(
                    '<td class="hpad"><table>'
                    + ('<tr><td class="vfill"></td></tr>' * (2 + 6))
                    + "</table></td>"
                )
            v.pop()
            a("</tr>")

            # horizontal space between month
            pad = [
                "<td><table><tr>"
                + ('<td class="hfill"></td>' * 7)
                + "</tr></table></td>",
                '<td class="vpad"><table><tr><td class="vfill hfill"></td></tr></table></td>',
            ] * (width - 1)
            a('\n<tr class="vpad">' + "".join(pad) + "</tr>\n")

        v.pop()
        a("</table>")
        return "".join(v)

    def formatyearpage(
        self,
        theyear,
        width=3,
        css="calendar.css",
        css_content=None,
        encoding=None,
        holidays=False,
        calendar=True,
    ):
        """
        Return a formatted year as a complete HTML page.
        """
        if encoding is None:
            encoding = sys.getdefaultencoding()
        v = []
        a = v.append
        a('<?xml version="1.0" encoding="%s"?>\n' % encoding)
        a(
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'
        )
        a("<html>\n")
        a("<head>\n")
        a(
            '<meta http-equiv="Content-Type" content="text/html; charset=%s" />\n'
            % encoding
        )
        if css is not None:
            a('<link rel="stylesheet" type="text/css" href="%s" />\n' % css)
        if css_content:
            a("<style>\n")
            a(css_content)
            a("</style>\n")
        if calendar:
            a("<title>Calendar for %d</title>\n" % theyear)
        if not calendar and holidays:
            a("<title>Holidays for %d</title>\n" % theyear)
        a("</head>\n")
        a("<body>\n")
        if calendar:
            a(self.formatyear(theyear, width))
        if holidays:
            a("<p />")
            a(self.formatholidays(theyear))
        a("</body>\n")
        a("</html>\n")
        return "".join(v).encode(encoding, "xmlcharrefreplace")
