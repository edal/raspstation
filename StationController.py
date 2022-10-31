import logging

from StationParameters import StationParameters
from StationStatus import StationStatus


class StationController:
    # Configurable vars
    TEMP_GPIO: int
    HEAT_GPIO: int
    FAN_GPIO: int
    FAN_PWM_GPIO: int

    # internal state
    status: StationStatus = None
    parameters: StationParameters = None

    def __init__(self, temp_gpio, heat_gpio, fan_gpio, fan_pwm_gpio, parameters: StationParameters):
        logging.debug('StationController init')
        self.TEMP_GPIO = temp_gpio
        self.HEAT_GPIO = heat_gpio
        self.FAN_GPIO = fan_gpio
        self.FAN_PWM_GPIO = fan_pwm_gpio
        self.parameters = parameters

    def doControlCycle(self):
        logging.debug('New controller cycle')
        self.status = StationStatus(23.0, 90, True, 3, True)

    def getExecutionStatus(self):
        logging.debug('Getting execution status')
        return self.status


    def tearDown(self):
        # disableFan, Heat and humidifier
        logging.debug("Tearing down station controller")





