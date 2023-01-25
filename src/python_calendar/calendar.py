import os
import locale
import datetime
import calendar
import html

import click

from .holidays import Syukujitsu, Holidays


class MyHTMLCalendar(calendar.HTMLCalendar):
    """
    This calendar returns complete HTML pages.
    """

    cssclasses = ["day mon", "day tue", "day wed", "day thu", "day fri", "day sat", "day sun"]
    cssclass_noday = "day noday"
    cssclasses_weekday_head = ["wd mon", "wd tue", "wd wed", "wd thu", "wd fri", "wd sat", "wd sun"]

    def __init__(self, firstweekday=0, startmonth=1):
        super().__init__(firstweekday)
        self.cur_year = None
        self.cur_month = None
        self.startmonth = startmonth
        self.holidays = Holidays()

    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            # day outside month
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            dt = datetime.date(self.cur_year, self.cur_month, day)
            holiday_name = self.holidays.get_holiday_name(dt)
            css = self.cssclasses[weekday]
            if holiday_name:
                css += ' holiday'
                name = html.escape(holiday_name, quote=True)
                return '<td class="%s" title="%s">%d</td>' % (css, name, day)
            else:
                return '<td class="%s">%d</td>' % (css, day)

    def formatweek(self, theweek):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        return '<tr class="days">%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % (
            self.cssclass_month))
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')

        # １月の行数を６週分固定にする
        arr = self.monthdays2calendar(theyear, themonth)
        arr = arr + [[(0,0)] * 7] * (6 - len(arr))

        for week in arr:
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatyear(self, theyear, width=3):
        """
        Return a formatted year as a table of tables.
        supports startmonth parameter.
        """
        v = []
        a = v.append
        width = max(width, 1)
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' %
          self.cssclass_year)
        a('\n')
        a('<tr><th colspan="%d" class="%s">%s</th></tr>' % (
            width + width - 1, self.cssclass_year_head, theyear))
        for i in range(self.startmonth, self.startmonth+12, width):
            # months in this row
            months = [((x - 1) % 12) + 1 for x in range(i, i+width)]
            a('<tr class="months-row">')
            for m in months:
                y = theyear + 1 if m < self.startmonth else theyear
                self.cur_year = y
                self.cur_month = m
                a('<td class="month">')
                a(self.formatmonth(y, m, withyear=False))
                a('</td>')
                # 月の左右の空白
                # NOTE: 単に <td></td> とすると excel に貼り付けたときに結合セルになってしまうので同じ個数の空セルで埋める。
                a('<td><table border="0" cellpadding="0" cellspacing="0" class="pad">' + ('<tr><td>&nbsp;</td></tr>' * (2+6)) + '</table></td>')
            v.pop()
            a('</tr>')

            # 月の列の上下の空白
            pad = ['<td><table border="0" cellpadding="0" cellspacing="0" class="pad">' + ('<td>&nbsp;</td>' * 7) + '</table></td>', '<td>&nbsp;</td>'] * width
            pad.pop()
            a('\n\n<tr>' + ''.join(pad) + '</tr>\n\n')

        v.pop()
        a('</table>')
        return ''.join(v)


@click.command()
@click.option('--year', default=datetime.date.today().year, help='target year')
@click.option('--filename', default='calendar.html', help='output HTML filename')
@click.option('--css', default='./calendar.css', help='css filename (link filename or URL)')
def main(year, filename, css):
    lc_time = os.getenv('LC_ALL') or os.getenv('LC_TIME') or os.getenv('LANG')
    locale.setlocale(locale.LC_TIME, lc_time)
    cal = MyHTMLCalendar(firstweekday=0, startmonth=4)
    year = 2023
    with open(filename, 'wb') as fh:
        fh.write(cal.formatyearpage(year, css=css))


if __name__ == '__main__':
    main()

