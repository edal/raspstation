import logging

import Adafruit_DHT

from StationParameters import StationParameters
from StationStatus import StationStatus


class StationController:
    # Configurable vars
    TEMP_GPIO: int
    HEAT_GPIO: int
    FAN_GPIO: int
    FAN_PWM_GPIO: int

    # Define default times in ticks/cycles (aprox 1 sec)
    DEFAULT_FAN_TICKS: int = 3
    DEFAUL_SENSOR_TICKS: int = 10

    MAX_TICKS: int = max(DEFAULT_FAN_TICKS, DEFAUL_SENSOR_TICKS)

    # internal state
    status: StationStatus = None
    parameters: StationParameters = None
    tick: int = 0

    def __init__(self, temp_gpio, heat_gpio, fan_gpio, fan_pwm_gpio, parameters: StationParameters):
        logging.debug('StationController init')
        self.TEMP_GPIO = temp_gpio
        self.HEAT_GPIO = heat_gpio
        self.FAN_GPIO = fan_gpio
        self.FAN_PWM_GPIO = fan_pwm_gpio
        self.parameters = parameters

    def doControlCycle(self):
        logging.debug('New controller cycle')
        # Get current tick/cycle
        self.tick=(self.tick+1) % self.MAX_TICKS

        if (self.tick%self.DEFAUL_SENSOR_TICKS == 1):
            h, t = self.getSensorReading()
            self.status.temperature = t
            self.status.humidity = h


    def getExecutionStatus(self):
        logging.debug('Getting execution status')
        return self.status


    def tearDown(self):
        # disableFan, Heat and humidifier
        logging.debug("Tearing down station controller")

    def getSensorReading(self):
        sensor=Adafruit_DHT.DHT11
        return Adafruit_DHT.read_retry(sensor, self.TEMP_GPIO)



