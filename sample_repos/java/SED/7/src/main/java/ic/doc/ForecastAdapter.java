package ic.doc;

import com.weather.Forecast;

public class ForecastAdapter implements WeatherForecast {

  private final Forecast forecast;

  public ForecastAdapter(Forecast forecast) {
    this.forecast = forecast;
  }

  public String summary() {
    return forecast.summary();
  }

  public int temperature() {
    return forecast.temperature();
  }
}