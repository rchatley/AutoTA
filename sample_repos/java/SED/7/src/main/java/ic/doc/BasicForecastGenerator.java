package ic.doc;

public class BasicForecastGenerator implements ForecastGenerator {

  private final ForecastGenerator forecaster;

  public BasicForecastGenerator(ForecastGenerator forecaster) {
    this.forecaster = forecaster;
  }

  @Override
  public WeatherForecast forecastFor(WeatherRegion region, WeatherDay day) {
    return forecaster.forecastFor(region, day);
  }
}
