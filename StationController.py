import logging

import Adafruit_DHT
import RPi.GPIO as GPIO

from StationParameters import StationParameters
from StationStatus import StationStatus


class StationController:
    # Configurable vars
    TEMP_GPIO: int
    HEAT_GPIO: int
    FAN_GPIO: int
    FAN_PWM_GPIO: int

    # Define default times in ticks/cycles (aprox 1 sec)
    DEFAULT_FAN_TICKS: int = 9
    DEFAUL_SENSOR_TICKS: int = 10

    # Default fan speed
    DEFAULT_FAN_SPEED: int = 100

    MAX_TICKS: int = max(DEFAULT_FAN_TICKS, DEFAUL_SENSOR_TICKS, DEFAULT_FAN_TICKS)

    # internal state
    status: StationStatus = StationStatus(0.0, 0, False, 0, False)
    parameters: StationParameters = None
    tick: int = 0

    fan_speed =  None


    def __init__(self, temp_gpio, heat_gpio, fan_gpio, fan_pwm_gpio, parameters: StationParameters):
        logging.debug('StationController init')
        self.TEMP_GPIO = temp_gpio
        self.HEAT_GPIO = heat_gpio
        self.FAN_GPIO = fan_gpio
        self.FAN_PWM_GPIO = fan_pwm_gpio
        self.parameters = parameters
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.FAN_PWM_GPIO, GPIO.OUT)
        self.fan_speed = GPIO.PWM(self.FAN_PWM_GPIO, self.DEFAULT_FAN_SPEED)
        self.fan_speed.start(self.DEFAULT_FAN_SPEED)

        GPIO.setup(self.FAN_GPIO, GPIO.OUT)
        GPIO.output(self.FAN_GPIO, GPIO.LOW)
        GPIO.setup(self.HEAT_GPIO, GPIO.OUT)
        GPIO.output(self.HEAT_GPIO, True) # off


    def doControlCycle(self):
        # Get current tick/cycle
        self.tick=(self.tick+1) % self.MAX_TICKS

        # Only read from sensor when at least DEFAUL_SENSOR_TICKS have passed (min each 2 ticks)
        if (self.tick%self.DEFAUL_SENSOR_TICKS == 1):
            h, t = self.__getSensorReading()
            self.status.previousTemperature = self.status.temperature
            self.status.previousHumidity = self.status.humidity
            self.status.temperature = t
            self.status.humidity = h
            logging.debug('New data read: Temp: %s Humidity: %s', '{:0.1f}'.format(t), '{:.0f}'.format(h))
            if (t < self.parameters.MIN_TEMPERATURE):
                logging.debug("Temperature is lower than MIN %s", self.parameters.MIN_TEMPERATURE)
                self.startHeat()
                self.stopFan()

            if (t >= self.parameters.MIN_TEMPERATURE and t < self.parameters.MAX_TEMPERATURE):
                logging.debug("Temperature is in range MIN-MAX %s-%s", self.parameters.MIN_TEMPERATURE, self.parameters.MAX_TEMPERATURE)
                self.stopFan()
                self.stopHeat()

            if (t >= self.parameters.MAX_TEMPERATURE):
                logging.debug("Temperature is greater than MAX %s", self.parameters.MAX_TEMPERATURE)
                self.__scheduleFans()

        self.__checkScheduling()


    def getExecutionStatus(self):
        return self.status

    def __scheduleFans(self, duration: int = -1):
        if (duration <= 0):
            duration = self.DEFAULT_FAN_TICKS

        # Only when there's no current schedule
        if (self.status.fanScheduledTicks == 0):
            self.status.fanScheduledTicks = duration
            self.startFan()

    def __checkScheduling(self):
        if (self.status.fanScheduledTicks == 1):
            # Last cycle for scheduled fans, stop them
            self.stopFan()

        # Decrease scheduled fan time one cycle
        if (self.status.fanScheduledTicks > 0):
            logging.debug('Fan remaining ticks %s', self.status.fanScheduledTicks)
            self.status.fanScheduledTicks-=1


    def startFan(self):
        if (not self.status.isFanEnabled):
            logging.debug('Starting fans')

            if (speed <= 0.0):
                speed = self.DEFAULT_FAN_SPEED

            GPIO.output(self.FAN_GPIO, GPIO.HIGH) # on
            self.status.isFanEnabled=True
            logging.debug('Fans started')

    def stopFan(self):
        if (self.status.isFanEnabled):
            logging.debug('Stopping fans')
            GPIO.output(self.FAN_GPIO, GPIO.LOW) # on
            self.status.isFanEnabled=False
            logging.debug('Fans stopped')

    def startHeat(self):
        if (not self.status.isHeatEnabled):
            logging.debug('Starting heating')
            GPIO.output(self.HEAT_GPIO, False) # Start
            self.status.isHeatEnabled=True
            logging.debug('Heating started')

    def stopHeat(self):
        if (self.status.isHeatEnabled):
            logging.debug('Stopping heating')
            GPIO.output(self.HEAT_GPIO, True) # Stop
            self.status.isHeatEnabled=False
            logging.debug('Heating stopped')

    def tearDown(self):
        # disableFan, Heat and humidifier
        logging.debug("Tearing down station controller")
        self.stopFan()
        self.stopHeat()
        GPIO.cleanup()

    def __getSensorReading(self):
        sensor=Adafruit_DHT.DHT11
        return Adafruit_DHT.read_retry(sensor, self.TEMP_GPIO)



