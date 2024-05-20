from src.forecast_generator import ForecastGenerator
from src.forecast_adapter import ForecastAdapter


class ForecasterAdapter(ForecastGenerator):
    def __init__(self, forecaster):
        self.forecaster = forecaster

    def forecast_for(self, region, day):
        forecast = self.forecaster.forecast_for(region.get_region(),
                                                day.get_day())
        return ForecastAdapter(forecast)
