import logging
import signal
import time

from DisplayController import DisplayController
from Program import Program
from ProgramController import ProgramController
from StationController import StationController
from StationParameters import StationParameters

# PARAMETERS
p1=Program('P1','Initial', StationParameters(23.0, 25.0, 90, 100, 1))
p2=Program('P2','Primordium', StationParameters(23.0, 25.0, 80, 90, 2))
p3=Program('P3','Grow', StationParameters(23.0, 25.0, 80, 90, 4))

programs = [p1, p2, p3]

# HARDWARE CONFIG
TEMP_GPIO=23 # BOARD16
HEAT_GPIO = 24 # BOARD18
FAN_PWM_GPIO = 18 # BOARD12
FAN_GPIO = 17 # BOARD11


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG, datefmt='%d-%m-%y %H:%M:%S')

# Script init
def init():
    global display,controller,programmer

    # Initialize main vars
    display = DisplayController()
    controller = StationController(TEMP_GPIO, HEAT_GPIO, FAN_GPIO, FAN_PWM_GPIO, programs[0])
    programmer = ProgramController(programs, display, controller)

# Script setup
def setup():
    # Check for saved program, display and await timeout or change
    programmer.setup()


# Each loop executes this method
def doCycle():
    controller.doControlCycle()
    status = controller.getExecutionStatus()
    display.syncDisplay(status, programmer.getCurrentParameters())

# Nicely handle exit (Ctrl+C, kill signal, exception, etc)
exiting=False
def handle_exit(signum=0, frame=0):
    global exiting
    if (exiting==False):
        exiting=True
        display.tearDown()
        controller.tearDown()
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
