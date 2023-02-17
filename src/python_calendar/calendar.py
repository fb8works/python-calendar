import calendar
import datetime
import html

import holidays


class HTMLCalendar(calendar.HTMLCalendar):
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
        self, firstweekday=0, startmonth=1, country=None, financial=None, subdiv=None
    ):
        super().__init__(firstweekday)
        self.cur_year = None
        self.cur_month = None
        self.startmonth = startmonth
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
            if holiday_name:
                css += " holiday"
                name = html.escape(holiday_name, quote=True)
                return '<td class="%s" title="%s"><div>%d</div></td>' % (css, name, day)
            else:
                return '<td class="%s">%d</td>' % (css, day)

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
        for i in range(self.startmonth, self.startmonth + 12, width):
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
