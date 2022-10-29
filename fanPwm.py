import random
import time
from time import sleep

from gpiozero import LED, PWMLED

# Set the PWM output we are using for the fan
FAN_PIN = "BOARD12"

fan = PWMLED(FAN_PIN)

