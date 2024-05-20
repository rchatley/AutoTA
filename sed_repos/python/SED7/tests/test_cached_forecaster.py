import unittest
from unittest.mock import Mock
from src.cached_forecaster import CachedForecaster
from src.weather_region import WeatherRegion
from src.weather_day import WeatherDay


class TestCachedForecaster(unittest.TestCase):
    def test_forecast_for_calls_correct_method(self):
        forecaster = Mock()
        generator = CachedForecaster(forecaster, 10)

        generator.forecast_for(WeatherRegion.LONDON, WeatherDay.MONDAY)
        generator.forecast_for(WeatherRegion.BIRMINGHAM, WeatherDay.WEDNESDAY)
        generator.forecast_for(WeatherRegion.SOUTH_EAST_ENGLAND,
                               WeatherDay.SUNDAY)

        forecaster.forecast_for.assert_any_call(WeatherRegion.LONDON,
                                                WeatherDay.MONDAY)
        forecaster.forecast_for.assert_any_call(WeatherRegion.BIRMINGHAM,
                                                WeatherDay.WEDNESDAY)
        forecaster.forecast_for.assert_any_call(
            WeatherRegion.SOUTH_EAST_ENGLAND, WeatherDay.SUNDAY)

    def test_forecast_for_calls_only_once(self):
        forecaster = Mock()
        generator = CachedForecaster(forecaster, 10)

        generator.forecast_for(WeatherRegion.LONDON, WeatherDay.MONDAY)
        generator.forecast_for(WeatherRegion.LONDON, WeatherDay.MONDAY)
        generator.forecast_for(WeatherRegion.LONDON, WeatherDay.MONDAY)

        self.assertEqual(forecaster.forecast_for.call_count, 1)
        forecaster.forecast_for.assert_any_call(WeatherRegion.LONDON,
                                                WeatherDay.MONDAY)


if __name__ == '__main__':
    unittest.main()
