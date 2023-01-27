import itertools
from typing import Dict


class HolidayBase:
    CONVERT: Dict[str, str] = {}

    def __init__(self):
        self.cache = {}
        self.cache_by_date = {}

    def _get_by_year(self, year):
        raise NotImplementedError()

    def normalize_item(self, item):
        if self.CONVERT is not None:
            try:
                item = (item[0], self.CONVERT[item[1]])
            except KeyError:
                pass
        return item

    def get_by_year(self, year):
        if year not in self.cache:
            self.cache[year] = list(sorted(self._get_by_year(year), key=lambda x: x[0]))
            self.cache_by_date = dict(self.cache[year])
        return self.cache[year]

    def get_holiday_name(self, date):
        self.get_by_year(date.year)
        return self.cache_by_date.get(date)

    def get_by_years(self, years):
        return list(itertools.chain.from_iterable([self.get_by_year(y) for y in years]))

    def format_item(self, item):
        return "{} {}".format(item[0].strftime("%Y/%m/%d"), item[1])
