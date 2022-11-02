class StationStatus:
    temperature: float
    humidity: int
    isFanEnabled: bool
    fanScheduledTicks: int
    isHeatEnabled: bool
    isHumidifierEnabled: bool
    humidifierScheduledTicks: int
    previousTemperature: float
    previousHumidity: int


    # Default constructor
    def __init__(self, temperature=0.0, humidity=0, isFanEnabled=False, fanScheduledTicks=0, isHeatEnabled=False, ifHumidifierEnabled=False, humidifierScheduledTicks=0):
        self.temperature=temperature
        self.humidity=humidity
        self.isFanEnabled=isFanEnabled
        self.fanScheduledTicks=fanScheduledTicks
        self.isHeatEnabled=isHeatEnabled
        self.ifHumidifierEnabled=ifHumidifierEnabled
        self.humidifierScheduledTicks=humidifierScheduledTicks

