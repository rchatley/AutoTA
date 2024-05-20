from enum import Enum
from lib.weather import Day


class WeatherDay(Enum):
    MONDAY = Day.MONDAY
    TUESDAY = Day.TUESDAY
    WEDNESDAY = Day.WEDNESDAY
    THURSDAY = Day.THURSDAY
    FRIDAY = Day.FRIDAY
    SATURDAY = Day.SATURDAY
    SUNDAY = Day.SUNDAY

    def get_day(self):
        return self.value
