import holidays

from .holiday_base import HolidayBase


class Holidays(HolidayBase):
    CONVERT = {
        "振替休日": "休日",
        "国民の休日": "休日",
        "休日（祝日扱い）": "休日",
        "天皇の即位の日": "休日",
        "即位礼正殿の儀が行われる日": "休日",
        "大喪の礼": "休日",
        "体育の日": "スポーツの日",
    }

    def _get_by_year(self, year):
        return holidays.JP(years=[year]).items()
