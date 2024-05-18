package ic.doc;

import com.weather.Forecaster;

public class ForecasterWrapper implements ForecastGenerator {

  private final Forecaster forecaster;

  public ForecasterWrapper(Forecaster forecaster) {
    this.forecaster = forecaster;
  }

  @Override
  public WeatherForecast forecastFor(WeatherRegion region, WeatherDay day) {
    return new ForecastWrapper(forecaster.forecastFor(region.getRegion(), day.getDay()));
  }
}