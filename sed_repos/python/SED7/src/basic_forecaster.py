from src.forecast_generator import ForecastGenerator


class BasicForecaster(ForecastGenerator):
    def __init__(self, forecaster):
        self.forecaster = forecaster

    def forecast_for(self, region, day):
        return self.forecaster.forecast_for(region, day)
