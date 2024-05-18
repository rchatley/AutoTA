package ic.doc;

public class BasicForecaster implements ForecastGenerator {

  private final ForecastGenerator forecaster;

  public BasicForecaster(ForecastGenerator forecaster) {
    this.forecaster = forecaster;
  }

  @Override
  public WeatherForecast forecastFor(WeatherRegion region, WeatherDay day) {
    return forecaster.forecastFor(region, day);
  }
}
