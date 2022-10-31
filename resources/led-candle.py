import random
import time

import RPi.GPIO as GPIO

# Set the PWM output we are using for the LED
LED = 18 #"BOARD12"

def setup():
    global pwm
    # GPIO uses broadcom numbering (GPIO numbers)
    GPIO.setmode(GPIO.BCM)
    # Set the LED pin as an output
    GPIO.setup(LED, GPIO.OUT)
    # Start PWM on the LED pin at 200Hz with a# 100% duty cycle. At lower frequencies the LED
    # would flicker even when we wanted it on solidly
    pwm = GPIO.PWM(LED, 200)

    # Start at a brightness of 100%
    pwm.start(100)

def set_brightness(new_brightness):
    # Sets brightness of the LED by changing duty cycle
    pwm.ChangeDutyCycle(new_brightness)

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
