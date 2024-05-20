from enum import Enum
from lib.weather import Region


class WeatherRegion(Enum):
    BIRMINGHAM = Region.BIRMINGHAM
    EDINBURGH = Region.EDINBURGH
    GLASGOW = Region.GLASGOW
    LONDON = Region.LONDON
    MANCHESTER = Region.MANCHESTER
    NORTH_ENGLAND = Region.NORTH_ENGLAND
    SOUTH_WEST_ENGLAND = Region.SOUTH_WEST_ENGLAND
    SOUTH_EAST_ENGLAND = Region.SOUTH_EAST_ENGLAND
    WALES = Region.WALES

    def get_region(self):
        return self.value
