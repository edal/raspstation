import logging
import time

import Adafruit_DHT
import RPi.GPIO as GPIO

from StationParameters import StationParameters
from StationStatus import StationStatus


class StationController:
    log = logging.getLogger('StationController')
    # Configurable vars
    TEMP_GPIO: int
    HEAT_GPIO: int
    FAN_GPIO: int
    FAN_PWM_GPIO: int
    HUMIDIFIER_GPIO: int

    # Define default times in ticks/cycles (aprox 1 sec)
    DEFAULT_FAN_TICKS: int = 4
    DEFAUL_SENSOR_TICKS: int = 10
    DEFAULT_HUMIDITY_TICKS: int = 2

    # Default fan speed
    DEFAULT_FAN_SPEED: int = 100

    MAX_TICKS: int = max(DEFAULT_FAN_TICKS, DEFAUL_SENSOR_TICKS, DEFAULT_FAN_TICKS, DEFAULT_HUMIDITY_TICKS)

    # internal state
    status: StationStatus = StationStatus(0.0, 0, False, 0, False)
    parameters: StationParameters = None
    tick: int = 0

    fan_speed =  None


    def __init__(self, temp_gpio, heat_gpio, fan_gpio, fan_pwm_gpio, humidifier_gpio, parameters: StationParameters):
        self.log.debug('StationController init')
        self.TEMP_GPIO = temp_gpio
        self.HEAT_GPIO = heat_gpio
        self.FAN_GPIO = fan_gpio
        self.FAN_PWM_GPIO = fan_pwm_gpio
        self.HUMIDIFIER_GPIO = humidifier_gpio
        self.parameters = parameters
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.FAN_PWM_GPIO, GPIO.OUT)
        self.fan_speed = GPIO.PWM(self.FAN_PWM_GPIO, self.DEFAULT_FAN_SPEED)
        self.fan_speed.start(self.DEFAULT_FAN_SPEED)

        GPIO.setup(self.FAN_GPIO, GPIO.OUT)
        GPIO.output(self.FAN_GPIO, GPIO.LOW)
        GPIO.setup(self.HEAT_GPIO, GPIO.OUT)

        GPIO.setup(self.HUMIDIFIER_GPIO, GPIO.OUT)
        GPIO.output(self.HUMIDIFIER_GPIO, GPIO.LOW)

    def setParameters(self, parameters: StationParameters):
        self.parameters = parameters

    def doControlCycle(self):
        # Get current tick/cycle
        self.tick=(self.tick+1) % self.MAX_TICKS

        # Check active schedulings before reads
        self.__checkScheduling()

        # Only read from sensor when at least DEFAUL_SENSOR_TICKS have passed (min each 2 ticks)
        if (self.tick%self.DEFAUL_SENSOR_TICKS == 1):
            h, t = self.__getSensorReading()
            self.status.previousTemperature = self.status.temperature
            self.status.previousHumidity = self.status.humidity
            self.status.temperature = t
            self.status.humidity = h
            self.log.debug('New data read: Temp: %s Humidity: %s', '{:0.1f}'.format(t), '{:.0f}'.format(h))
            if (t < self.parameters.MIN_TEMPERATURE):
                self.log.debug("Temperature is lower than MIN %s", self.parameters.MIN_TEMPERATURE)
                self.startHeat()
                self.stopFan()

            if (t >= self.parameters.MIN_TEMPERATURE):
                self.log.debug("Temperature is major than min MIN-MAX %s-%s", self.parameters.MIN_TEMPERATURE, self.parameters.MAX_TEMPERATURE)
                self.stopHeat()

            if ( t < self.parameters.MAX_TEMPERATURE):
                self.log.debug("Temperature is lower than max MIN-MAX %s-%s", self.parameters.MIN_TEMPERATURE, self.parameters.MAX_TEMPERATURE)
                self.stopFan()

            if (t >= self.parameters.MAX_TEMPERATURE):
                self.log.debug("Temperature is greater than MAX %s", self.parameters.MAX_TEMPERATURE)
                self.__scheduleFans()

            if (h < self.parameters.MIN_HUMIDITY):
                self.log.debug("Humidity is lower than MIN %s", self.parameters.MIN_HUMIDITY)
                self.__scheduleHumidifier()

            if (h >= self.parameters.MIN_HUMIDITY and h < self.parameters.MAX_HUMIDITY):
                self.log.debug("Humidity is in range MIN-MAX %s-%s", self.parameters.MIN_HUMIDITY, self.parameters.MAX_HUMIDITY)

            if (h >= self.parameters.MAX_HUMIDITY):
                self.log.debug("Humidity is greater than MAX %s", self.parameters.MIN_HUMIDITY)
                self.__scheduleFans()

            self.status.inRange=(t >= self.parameters.MIN_TEMPERATURE and t < self.parameters.MAX_TEMPERATURE) and (h >= self.parameters.MIN_HUMIDITY and h < self.parameters.MAX_HUMIDITY)


    def getExecutionStatus(self):
        return self.status

    def __scheduleFans(self, duration: int = -1):
        if (duration <= 0):
            duration = self.DEFAULT_FAN_TICKS

        # Only when there's no current schedule
        if (self.status.fanScheduledTicks == 0):
            self.status.fanScheduledTicks = duration
            self.startFan()

    def __scheduleHumidifier(self, duration: int = -1):
        if (duration <= 0):
            duration = self.DEFAULT_HUMIDITY_TICKS

        # Only when there's no current schedule
        if (self.status.humidifierScheduledTicks == 0):
            self.status.humidifierScheduledTicks = duration
            self.startHumidifier()


    def __checkScheduling(self):
        if (self.status.fanScheduledTicks > 0):
            # Decrease scheduled fan time one cycle
            self.status.fanScheduledTicks-=1
            self.log.debug('Fan remaining ticks %s', self.status.fanScheduledTicks)

            if (self.status.fanScheduledTicks == 0):
                # Last cycle for scheduled fans, stop them
                self.stopFan()

        if (self.status.humidifierScheduledTicks > 0):
            # Decrease scheduled time one cycle
            self.status.humidifierScheduledTicks-=1
            self.log.debug('Humidifier remaining ticks %s', self.status.humidifierScheduledTicks)

            if (self.status.humidifierScheduledTicks == 0):
                # Last cycle, stop it
                self.stopHumidifier()


    def startFan(self):
        if (not self.status.isFanEnabled):
            self.log.debug('Starting fans')
            GPIO.output(self.FAN_GPIO, GPIO.HIGH) # on
            self.status.isFanEnabled=True
            self.log.debug('Fans started')

    def stopFan(self):
        if (self.status.isFanEnabled):
            self.log.debug('Stopping fans')
            GPIO.output(self.FAN_GPIO, GPIO.LOW) # on
            self.status.isFanEnabled=False
            self.log.debug('Fans stopped')

    def startHeat(self):
        if (not self.status.isHeatEnabled):
            self.log.debug('Starting heating')
            GPIO.output(self.HEAT_GPIO, False) # Start
            self.status.isHeatEnabled=True
            self.log.debug('Heating started')

    def stopHeat(self):
        if (self.status.isHeatEnabled):
            self.log.debug('Stopping heating')
            GPIO.output(self.HEAT_GPIO, True) # Stop
            self.status.isHeatEnabled=False
            self.log.debug('Heating stopped')

    def startHumidifier(self):
        if (not self.status.isHumidifierEnabled):
            self.log.debug('Starting humidifier')
            GPIO.output(self.HUMIDIFIER_GPIO, GPIO.HIGH) # Start
            self.status.isHumidifierEnabled=True
            self.log.debug('Humidifier started')

    def stopHumidifier(self):
        if (self.status.isHumidifierEnabled):
            self.log.debug('Stopping humidifier')
            GPIO.output(self.HUMIDIFIER_GPIO, GPIO.LOW) # Start
            self.status.isHumidifierEnabled=False
            self.log.debug('Humidifier stopped')

    def tearDown(self):
        # disableFan, Heat and humidifier
        self.log.debug("Tearing down station controller")
        self.stopFan()
        self.stopHeat()
        GPIO.cleanup()

    def __getSensorReading(self):
        sensor=Adafruit_DHT.DHT11
        return Adafruit_DHT.read_retry(sensor, self.TEMP_GPIO)



