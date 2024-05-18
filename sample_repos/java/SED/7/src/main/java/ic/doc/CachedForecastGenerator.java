package ic.doc;

import ic.doc.lib.Pair;

import java.util.Map;
import java.util.HashMap;
import java.util.Collection;

public class CachedForecastGenerator implements ForecastGenerator {

  private static final int DEFAULT_CACHE_SIZE = 5;
  public static final long CACHE_TIMEOUT_MILLIS = 3600000;

  private final ForecastGenerator forecaster;
  private final Map<Pair<WeatherRegion, WeatherDay>, Pair<WeatherForecast, Long>> forecastCache
      = new HashMap<>();
  private final int maxCacheSize;

  public CachedForecastGenerator(ForecastGenerator forecaster) {
    this.forecaster = forecaster;
    this.maxCacheSize = DEFAULT_CACHE_SIZE;
  }

  public CachedForecastGenerator(ForecastGenerator forecaster, int maxCacheSize) {
    this.forecaster = forecaster;
    if (maxCacheSize < 0) {
      maxCacheSize = 0;
    }
    this.maxCacheSize = maxCacheSize;
  }

  public WeatherForecast forecastFor(WeatherRegion region, WeatherDay day) {
    Pair<WeatherForecast, Long> forecastPair = forecastCache.get(new Pair<>(region, day));
    WeatherForecast forecast;

    if (forecastPair == null || System.currentTimeMillis() > forecastPair.value()) {
      // Refresh from forecaster
      forecast = forecaster.forecastFor(region, day);

      // Add to cache
      if (maxCacheSize > 0) {
        if (forecastCache.size() == maxCacheSize) {
          // Remove oldest element
          Pair<WeatherForecast, Long> elemToRemove = getOldestElement();
          forecastCache.remove(elemToRemove);
        }
        forecastCache.put(
            new Pair<>(region, day),
            new Pair<>(forecast, System.currentTimeMillis() + CACHE_TIMEOUT_MILLIS));
      }
    } else {
      forecast = forecastPair.key();
    }

    if (forecast == null) {
      throw new RuntimeException("Could not find a forecast for the given Area / Day");
    }

    return forecast;
  }

  private Pair<WeatherForecast, Long> getOldestElement() {
    Collection<Pair<WeatherForecast, Long>> valSet = forecastCache.values();

    return valSet.stream().reduce((a, b) -> (a.value() > b.value() ? a : b)).orElse(null);
  }
}
