package ic.doc;

import com.weather.Forecaster;

public class ForecasterAdapter implements ForecastGenerator {

  private final Forecaster forecaster;

  public ForecasterAdapter(Forecaster forecaster) {
    this.forecaster = forecaster;
  }

  @Override
  public WeatherForecast forecastFor(WeatherRegion region, WeatherDay day) {
    return new ForecastAdapter(forecaster.forecastFor(region.getRegion(), day.getDay()));
  }
}