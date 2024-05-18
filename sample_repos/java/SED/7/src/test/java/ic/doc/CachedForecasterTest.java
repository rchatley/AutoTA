package ic.doc;

import org.jmock.Expectations;
import org.jmock.Mockery;
import org.junit.Test;

public class CachedForecasterTest {

  Mockery context = new Mockery();
  ForecastGenerator forecaster = context.mock(ForecastGenerator.class);

  @Test
  public void forecastForCallsCorrectMethod() {
    ForecastGenerator generator = new CachedForecaster(forecaster, 10);

    context.checking(new Expectations() {{
      exactly(1).of(forecaster).forecastFor(
              WeatherRegion.LONDON, WeatherDay.MONDAY);
      exactly(1).of(forecaster).forecastFor(
              WeatherRegion.BIRMINGHAM, WeatherDay.WEDNESDAY);
      exactly(1).of(forecaster).forecastFor(
              WeatherRegion.SOUTH_EAST_ENGLAND, WeatherDay.SUNDAY);
    }});

    generator.forecastFor(WeatherRegion.LONDON, WeatherDay.MONDAY);
    generator.forecastFor(WeatherRegion.BIRMINGHAM, WeatherDay.WEDNESDAY);
    generator.forecastFor(WeatherRegion.SOUTH_EAST_ENGLAND, WeatherDay.SUNDAY);

  }

  @Test
  public void forecastForCallsOnlyOnce() {
    ForecastGenerator generator = new CachedForecaster(forecaster, 10);

    context.checking(new Expectations() {{
      exactly(1).of(forecaster).forecastFor(WeatherRegion.LONDON, WeatherDay.MONDAY);
    }});


    generator.forecastFor(WeatherRegion.LONDON, WeatherDay.MONDAY);
    generator.forecastFor(WeatherRegion.LONDON, WeatherDay.MONDAY);
    generator.forecastFor(WeatherRegion.LONDON, WeatherDay.MONDAY);
  }
}

