import random
import time

import RPi.GPIO as GPIO

# Set the PWM output we are using for the LED
RED = "BOARD12"
AMBER = "BOARD16"
GREEN = "BOARD18"

def setup():
    global red, amber, green

    # GPIO uses broadcom numbering (GPIO numbers)
    GPIO.setmode(GPIO.BCM)
    # Set the LED pin as an output
    GPIO.setup(RED, GPIO.OUT)
    GPIO.setup(AMBER, GPIO.OUT)
    GPIO.setup(GREEN, GPIO.OUT)

    # Start PWM on the LED pin at 200Hz with a# 100% duty cycle. At lower frequencies the LED
    # would flicker even when we wanted it on solidly
    red = GPIO.PWM(RED, 200)
    amber = GPIO.PWM(RED, 200)
    green = GPIO.PWM(RED, 200)

    # Start at a brightness of 100%
    red.start(100)
    amber.start(100)
    green.start(100)

def set_brightness(new_brightness):
    # Sets brightness of the LED by changing duty cycle
    red.ChangeDutyCycle(new_brightness)
    amber.ChangeDutyCycle(new_brightness)
    green.ChangeDutyCycle(new_brightness)

def flicker():
    # We want a random brightness between 0% and 100%.
    # Then then we’ll hold it for a random time
    # between 0.01 and 0.1 seconds to get a nice flicker
    # effect. Play with these values to make the effect
    # suit your liking
    set_brightness(random.randrange(0, 100))
    time.sleep(random.randrange(1, 10) *0.01)

# The wrapper around the flicker function makes sure the
# GPIO hardware is cleaned up when the user presses CTRL-C
def loop():
    try:
        while True:
            flicker()
    except KeyboardInterrupt:
       pass
    finally:
       GPIO.cleanup()

# setup the hardware
setup()

# start the flickering
loop()
