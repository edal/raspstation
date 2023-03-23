import logging

from CsvLogger import CsvLogger

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG, datefmt='%d-%m-%y %H:%M:%S')

import signal
import sys
import time

from DisplayController import DisplayController
from Program import Program
from ProgramController import ProgramController
from StationController import StationController
from StationParameters import StationParameters

# PARAMETERS
p1=Program('P1','Initial', StationParameters(23.0, 26.0, 90, 100, 0))
p2=Program('P2','Primordium', StationParameters(23.0, 26.0, 85, 100, 2))
p3=Program('P3','Grow', StationParameters(23.0, 26.0, 80, 92, 4))
y1=Program('Y1','Yeti.Initial', StationParameters(23.0, 26.0, 97, 100, 0))
nh=Program('H','Only heat', StationParameters(22.0, 26.0, 0, 100, 0))
ff=Program('FF','Force Fans', StationParameters(0.0, 40.0, 0, 10, 10))
hh=Program('HH','Turbo humidifier', StationParameters(0.0, 40.0, 99, 100, 0, 10))

programs = [p1, p2, p3, y1, nh, ff, hh]
# HARDWARE CONFIG
TEMP_GPIO=23 # BOARD16
HEAT_GPIO = 24 # BOARD18
FAN_PWM_GPIO = 18 # BOARD12
FAN_GPIO = 17 # BOARD11
HUMIDIFIER_GPIO=4 # BOARD7

BACKLIGHT_GPIO=27 # BOARD13
PROGRAM_SELECT=22 # BOARD15
log = logging.getLogger()


# Script init
def init():
    global display,controller,programmer,csvLog

    # Initialize main vars
    display = DisplayController()
    controller = StationController(TEMP_GPIO, HEAT_GPIO, FAN_GPIO, FAN_PWM_GPIO,HUMIDIFIER_GPIO, programs[0].parameters)

    programmer = ProgramController(programs, display, controller)
    csvLog = CsvLogger()

# Script setup
def setup():
    # Check for saved program, display and await timeout or change
    log.debug('Setting up programs...')
    programmer.setup()


# Each loop executes this method
def doCycle():
    controller.doControlCycle()
    status = controller.getExecutionStatus()
    display.syncDisplay(status, programmer.getCurrentParameters())
    csvLog.logStatus(status)

# Nicely handle exit (Ctrl+C, kill signal, exception, etc)
exiting=False
def handle_exit(signum=0, frame=0):
    global exiting
    if (exiting==False):
        exiting=True
        try:
            display.tearDown()
            controller.tearDown()
            programmer.tearDown()
        except:
            pass
        finally:
            exit(0)

# Link handle_exit method with kill signals
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

# The main loop
try:
    init()
    setup()
    while True:
        doCycle()
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    handle_exit()
