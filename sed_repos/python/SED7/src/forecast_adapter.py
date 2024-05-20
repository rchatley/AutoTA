class ForecastAdapter:
    def __init__(self, forecast):
        self.forecast = forecast

    def summary(self):
        return self.forecast.summary()

    def temperature(self):
        return self.forecast.temperature()
