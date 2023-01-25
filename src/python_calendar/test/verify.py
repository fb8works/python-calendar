from collections import defaultdict

import click
from prettytable import PrettyTable

from python_calendar.holidays import Syukujitsu, Holidays
from python_calendar.holidays.jpholiday import JPHoliday


def verify(*, normalize=False):
    """
    内閣府の提供する祝日データを元に holidays と jpholiday を検証します。

    normalize が True の場合は各パッケージの返す祝日の名前を一般化して比較します。
    """

    years = list(range(1955, 2023+1))
    classes = (Syukujitsu, Holidays, JPHoliday)

    # {<datetime.date>: [S1, H1, J1, S2, H2, J2]}
    # S1,H1,J1: original name. eg. "皇太子・皇太子徳仁親王の結婚の儀"
    # S2,H2,J2: normalized name. eg. "結婚の儀"
    name_by_date = defaultdict(lambda: [None] * (len(classes) * 2))

    for i, cls in enumerate(classes):
        instance = cls()
        data = instance.get_by_years(years)
        for item in data:
            dt, name = item
            name_by_date[dt][i] = name
            if normalize:
                name_by_date[dt][i+3] = instance.normalize_item(item)[1]

    table = PrettyTable()
    table.field_names = ['Date'] + [cls.__name__ for cls in classes]

    slicer = slice(0,3) if normalize else slice(3)

    for dt, names in sorted(name_by_date.items(), key=lambda x: x[0]):
        if len(set(names[slicer])) != 1:
            value = [x if x is not None else '-' for x in names[:3]]
            table.add_row([dt] + value)

    print(table)


@click.command()
@click.option("--normalize", is_flag=True, show_default=True, default=False, help="validate with normalize holiday name")
def main(normalize):
    verify(normalize=False)


if __name__ == '__main__':
    main()

