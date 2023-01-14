import logging


class StationStatus:
    temperature: float
    humidity: float
    isFanEnabled: bool
    fanScheduledTicks: int
    isHeatEnabled: bool
    isHumidifierEnabled: bool
    humidifierScheduledTicks: int
    previousTemperature: float
    previousHumidity: float
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

    def equals(self, other):
        try:
            return (other is not None) and (self.temperature==other.temperature and
                    self.humidity==other.humidity and
                    self.isFanEnabled==other.isFanEnabled and
                    #self.fanScheduledTicks==other.fanScheduledTicks and
                    self.isHeatEnabled==other.isHeatEnabled and
                    self.isHumidifierEnabled==other.isHumidifierEnabled and
                    #self.humidifierScheduledTicks==other.humidifierScheduledTicks and
                    self.inRange==other.inRange)
        except Exception as e:
            print("An error ocurred comparing StationStatus objects: ", e)
            return False

    def print(self, name):
        logging.debug("%s: temp:%s hum:%s isFan:%s isHeat:%s isHum:%s inRange:%s" % (name, self.temperature,self.humidity,self.isFanEnabled,self.isHeatEnabled,self.isHumidifierEnabled,self.inRange))

    def clone(self):
        return  StationStatus(self.temperature, self.humidity, self.isFanEnabled, self.fanScheduledTicks, self.isHeatEnabled, self.isHumidifierEnabled, self.humidifierScheduledTicks, self.inRange)