from src.forecast_generator import ForecastGenerator


class CachedForecaster(ForecastGenerator):
    def __init__(self, forecaster, size):
        self.forecaster = forecaster
        self.cache = {}
        self.size = size

    def forecast_for(self, region, day):
        key = f"{region} : {day}"
        if key not in self.cache:
            forecast = self.forecaster.forecast_for(region, day)
            if forecast is None:
                raise RuntimeError("Could not find a forecast")
            if len(self.cache) >= self.size:
                self.cache.pop(next(iter(self.cache)))
            self.cache[key] = forecast
        return self.cache[key]
