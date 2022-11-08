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
    inRange: bool


    # Default constructor
    def __init__(self, temperature=0.0, humidity=0, isFanEnabled=False, fanScheduledTicks=0, isHeatEnabled=False, isHumidifierEnabled=False, humidifierScheduledTicks=0, inRange=True):
        self.temperature=temperature
        self.humidity=humidity
        self.isFanEnabled=isFanEnabled
        self.fanScheduledTicks=fanScheduledTicks
        self.isHeatEnabled=isHeatEnabled
        self.ifHumidifierEnabled=isHumidifierEnabled
        self.humidifierScheduledTicks=humidifierScheduledTicks
        self.inRange = inRange

