package ic.doc;

import com.weather.Region;

public enum WeatherRegion {
  BIRMINGHAM(Region.BIRMINGHAM),
  EDINBURGH(Region.EDINBURGH),
  GLASGOW(Region.GLASGOW),
  LONDON(Region.LONDON),
  MANCHESTER(Region.MANCHESTER),
  NORTH_ENGLAND(Region.NORTH_ENGLAND),
  SOUTH_WEST_ENGLAND(Region.SOUTH_WEST_ENGLAND),
  SOUTH_EAST_ENGLAND(Region.SOUTH_EAST_ENGLAND),
  WALES(Region.WALES);

  private final com.weather.Region region;

  WeatherRegion(com.weather.Region region) {
    this.region = region;
  }

  public Region getRegion() {
    return region;
  }
}

//public record WeatherRegion(Region region) {}
