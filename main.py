import logging
import signal
import time

from DisplayController import DisplayController
from StationController import StationController
from StationParameters import StationParameters

# PARAMETERS
MIN_TEMP=23.0
MAX_TEMP=25.0
MIN_HUMIDITY=85.0
MAX_HUMIDITY=98.0

# HARDWARE CONFIG
TEMP_GPIO=23 # BOARD16
HEAT_GPIO = 24 # BOARD18
FAN_PWM_GPIO = 18 # BOARD12
FAN_GPIO = 17 # BOARD11


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG, datefmt='%d-%m-%y %H:%M:%S')

# Script init
def init():
    global display,controller,parameters

    # Initialize main vars
    parameters = StationParameters(MIN_TEMP, MAX_TEMP, MIN_HUMIDITY, MAX_HUMIDITY)
    display = DisplayController()
    controller = StationController(TEMP_GPIO, FAN_GPIO, FAN_PWM_GPIO, HEAT_GPIO, parameters)


# Each loop executes this method
def doCycle():
    controller.doControlCycle()
    status = controller.getExecutionStatus()
    display.syncDisplay(status, parameters)

# Nicely handle exit
def handle_exit(signum=0, frame=0):
    display.tearDown()
    controller.tearDown()
    exit(0)

# Link handle_exit method with kill signals
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

# The main loop
try:
    init()
    while True:
        doCycle()
        time.sleep(1)
except:
    handle_exit()
