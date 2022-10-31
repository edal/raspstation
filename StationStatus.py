class StationStatus:
    temperature: float
    humidity: int
    isFanEnabled: bool
    fanScheduledTicks: int
    isHeatEnabled: bool
    isHumidifierEnabled: bool
    humidifierScheduledTicks: int


    # Default constructor
    def __init__(self, temperature, humidity, isFanEnabled, fanScheduledTicks, isHeatEnabled, ifHumidifierEnabled, humidifierScheduledTicks):
        self.temperature=temperature
        self.humidity=humidity
        self.isFanEnabled=isFanEnabled
        self.fanScheduledTicks=fanScheduledTicks
        self.isHeatEnabled=isHeatEnabled
        self.ifHumidifierEnabled=ifHumidifierEnabled
        self.humidifierScheduledTicks=humidifierScheduledTicks

    # Constructor without humidifier
    def __init__(self, temperature, humidity, isFanEnabled, fanScheduledTicks, isHeatEnabled):
        self.__init__(self, temperature, humidity, isFanEnabled, fanScheduledTicks, isHeatEnabled, False, 0)
