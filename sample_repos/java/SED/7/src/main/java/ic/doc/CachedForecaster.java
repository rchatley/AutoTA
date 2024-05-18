package ic.doc;

import java.util.LinkedHashMap;
import java.util.Map;

public class CachedForecaster implements ForecastGenerator {

  private final ForecastGenerator forecaster;
  private final Map<String, WeatherForecast> cache;

  public CachedForecaster(ForecastGenerator forecaster, int size) {
    this.forecaster = forecaster;

    this.cache = new LinkedHashMap<>() {
      protected boolean removeEldestEntry(Map.Entry<String, WeatherForecast> eldest) {
        return size() > size;
      }
    };
  }


  @Override
  public WeatherForecast forecastFor(WeatherRegion region, WeatherDay day) {
    String searchString = region + " : " + day.toString();
    WeatherForecast forecast = cache.get(searchString);
    if (forecast == null) {
      forecast = forecaster.forecastFor(region, day);
      cache.put(searchString, forecast);
    }

    if (forecast == null) {
      throw new RuntimeException("Could not find a forecast");
    }

    return forecast;
  }
}
