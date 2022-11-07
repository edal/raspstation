import logging
from math import ceil


class StationParameters:
    MAX_TEMPERATURE: float
    MIN_TEMPERATURE: float
    MAX_HUMIDITY: int
    MIN_HUMIDITY: int
    scheduledFansPerDay: int

    def __init__(self, minTemp: float, maxTemp: float, minHumi: int, maxHumi:int, scheduledFansPerDay:int=0):
        logging.debug("Initializing StationParameters")
        self.MAX_HUMIDITY=maxHumi
        self.MIN_HUMIDITY=minHumi
        self.MIN_TEMPERATURE=minTemp
        self.MAX_TEMPERATURE=maxTemp
        self.scheduledFansPerDay = scheduledFansPerDay
        if (scheduledFansPerDay == 0):
            self.fanCycleDelay = 0
        else:
            self.fanCycleDelay = ceil(86400 / scheduledFansPerDay)
