package ic.doc;

import com.weather.Forecaster;
import org.jmock.Expectations;
import org.jmock.Mockery;
import org.junit.Test;

public class CachedForecastGeneratorTest {

  Mockery context = new Mockery();
  ForecastGenerator forecaster = context.mock(ForecastGenerator.class);

  @Test
  public void forecastForCallsCorrectMethod() {
  ForecastGenerator generator = new CachedForecastGenerator(forecaster);

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
    ForecastGenerator generator = new CachedForecastGenerator(forecaster);

    context.checking(new Expectations() {{
      exactly(1).of(forecaster).forecastFor(WeatherRegion.LONDON, WeatherDay.MONDAY);
    }});


    generator.forecastFor(WeatherRegion.LONDON, WeatherDay.MONDAY);
    generator.forecastFor(WeatherRegion.LONDON, WeatherDay.MONDAY);
    generator.forecastFor(WeatherRegion.LONDON, WeatherDay.MONDAY);
  }


  @Test
  public void cachedForecasterFasterOrEqualToBasic() {
    BasicForecastGenerator basic =
        new BasicForecastGenerator(new ForecasterWrapper(new Forecaster()));
    CachedForecastGenerator cached =
        new CachedForecastGenerator(new ForecasterWrapper(new Forecaster()));

    long basicStart = System.currentTimeMillis();
    for (int i = 0; i < 2; i++) {
      basic.forecastFor(WeatherRegion.LONDON, WeatherDay.MONDAY);
      basic.forecastFor(WeatherRegion.BIRMINGHAM, WeatherDay.THURSDAY);
    }
    long basicTime = System.currentTimeMillis() - basicStart;

    long cachedStart = System.currentTimeMillis();
    for (int i = 0; i < 2; i++) {
      cached.forecastFor(WeatherRegion.LONDON, WeatherDay.MONDAY);
      cached.forecastFor(WeatherRegion.BIRMINGHAM, WeatherDay.THURSDAY);
    }

    long cachedTime = System.currentTimeMillis() - cachedStart;

    assert (cachedTime <= basicTime);
  }
}