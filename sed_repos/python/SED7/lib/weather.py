from enum import Enum


class Day(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class Region(Enum):
    BIRMINGHAM = 0
    EDINBURGH = 1
    GLASGOW = 2
    LONDON = 3
    MANCHESTER = 4
    NORTH_ENGLAND = 5
    SOUTH_WEST_ENGLAND = 6
    SOUTH_EAST_ENGLAND = 7
    WALES = 8
