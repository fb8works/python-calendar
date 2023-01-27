import csv
import datetime

from .holiday_base import HolidayBase


class Syukujitsu(HolidayBase):
    CONVERT = {
        "休日（祝日扱い）": "休日",
        "大喪の礼": "休日",
        "体育の日": "スポーツの日",
        "体育の日（スポーツの日）": "スポーツの日",
    }
    rows = None

    def __init__(self, filename="syukujitsu.csv"):
        super().__init__()
        self.csv_filename = filename

    def get_data(self):
        if self.rows is None:
            with open(self.csv_filename, encoding="cp932") as out:
                reader = csv.reader(out)
                next(reader, None)
                self.rows = [
                    (datetime.datetime.strptime(date, "%Y/%m/%d").date(), name)
                    for date, name in reader
                ]
        return self.rows

    def _get_by_year(self, year):
        dt1 = datetime.date(year, 1, 1)
        dt2 = datetime.date(year + 1, 1, 1)
        return [x for x in self.get_data() if dt1 <= x[0] < dt2]
