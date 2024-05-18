package ic.doc;

public interface ForecastGenerator {
  WeatherForecast forecastFor(WeatherRegion region, WeatherDay day);
}
