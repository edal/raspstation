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
        self.isHumidifierEnabled=isHumidifierEnabled
        self.humidifierScheduledTicks=humidifierScheduledTicks
        self.inRange = inRange

    def equals(self, other ):
        try:
            return other is not None and (self.temperature==other.temperature and
                    self.humidity==other.humidity and
                    self.isFanEnabled==other.isFanEnabled and
                    self.fanScheduledTicks==other.fanScheduledTicks and
                    self.isHeatEnabled==other.isHeatEnabled and
                    self.isHumidifierEnabled==other.isHumidifierEnabled and
                    self.humidifierScheduledTicks==other.humidifierScheduledTicks and
                    self.inRange==other.inRange)
        except:
            return False
