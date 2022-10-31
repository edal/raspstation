import random
import time
from time import sleep

from gpiozero import LED, PWMLED

# Set the PWM output we are using for the LED
RED = "BOARD16"
AMBER = "BOARD12"
GREEN = "BOARD18"

def setup():
    global red, amber, green

    amber = PWMLED(AMBER)
    green = PWMLED(GREEN)
    red = PWMLED(RED)

    # Start at a brightness of 100%
    green.on()
    sleep(0.3)
    green.off()
    amber.value=1.0


def set_brightness(new_brightness):
    # Sets brightness of the LED
    amber.value=new_brightness

def flicker():
    # We want a random brightness between 0% and 100%.
    # Then then we’ll hold it for a random time
    # between 0.01 and 0.1 seconds to get a nice flicker
    # effect. Play with these values to make the effect
    # suit your liking
    set_brightness(random.random())
    time.sleep(0.1-(random.random()*0.1))

# The wrapper around the flicker function makes sure the
# GPIO hardware is cleaned up when the user presses CTRL-C
def loop():
    try:
        while True:
            flicker()
    except KeyboardInterrupt:
       pass
    finally:
        red.on()
        sleep(0.3)
        red.off()


# setup the hardware
setup()

# start the flickering
loop()
