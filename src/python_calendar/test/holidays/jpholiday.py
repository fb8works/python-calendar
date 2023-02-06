import jpholiday

from .holiday_base import HolidayBase


class JPHoliday(HolidayBase):
    CONVERT = {
        "皇太子・明仁親王の結婚の儀": "結婚の儀",
        "皇太子・皇太子徳仁親王の結婚の儀": "結婚の儀",
        "即位の礼正殿の儀": "即位礼正殿の儀",
        "即位礼正殿の儀が行われる日": "休日",
        "即位礼正殿の儀": "休日",
        "昭和天皇の大喪の礼": "休日",
        "国民の休日": "休日",
        "天皇の即位の日": "休日",
        "体育の日": "スポーツの日",
    }

    def normalize_item(self, item):
        if item[1].endswith("振替休日"):
            return (item[0], "休日")
        return super().normalize_item(item)

    def _get_by_year(self, year):
        return [(k, v) for k, v in jpholiday.year_holidays(year)]
