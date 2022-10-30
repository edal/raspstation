import random
import time
from time import sleep

from gpiozero import LED, PWMLED

# Set the PWM output we are using for the fan
FAN_PWM_PIN = "BOARD12"
FAN_PIN = "BOARD11"

fan_speed = PWMLED(FAN_PWM_PIN)
fan = LED(FAN_PIN)
