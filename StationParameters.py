import logging


class StationParameters:
    MAX_TEMPERATURE: float
    MIN_TEMPERATURE: float
    MAX_HUMIDITY: int
    MIN_HUMIDITY: int

    def __init__(self):
        logging.debug("Initializing StationParameters")
        self.MAX_HUMIDITY=98
        self.MIN_HUMIDITY=80
        self.MIN_TEMPERATURE=23.0
        self.MAX_TEMPERATURE=25.0

    def __init__(self, minTemp: float, maxTemp: float, minHumi: int, maxHumi:int):
        logging.debug("Initializing StationParameters")
        self.MAX_HUMIDITY=maxHumi
        self.MIN_HUMIDITY=minHumi
        self.MIN_TEMPERATURE=minTemp
        self.MAX_TEMPERATURE=maxTemp
