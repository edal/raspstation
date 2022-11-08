import logging
import time
from os.path import exists

from DisplayController import DisplayController
from Program import Program
from StationController import StationController


class ProgramController:
    PROGRAM_FILE=".storedProgram"
    DEFAULT_TIMEOUT=5

    currentProgram: int
    programs = []
    display: DisplayController
    station: StationController
    remainingTimeout: int
    isDisplayingProgram: bool = False

    def __init__(self, programs, display: DisplayController, station: StationController):
        logging.debug('Initializing program controller')
        self.programs = programs
        self.display = display
        self.station = station
        self.currentProgram = 0
        logging.debug('Program controller initialized')

    def getCurrentParameters(self):
        logging.debug('Getting current program parameters...')
        return self.programs[self.currentProgram].parameters

    def setup(self):
        logging.debug('Entering program setup...')
        self.currentProgram=self.loadLastUsedProgramOrDefault()
        self.remainingTimeout=self.DEFAULT_TIMEOUT
        self.displayCurrentProgram()
        logging.debug('Program setup done')

    def onProgramButtonPress(self):
        self.currentProgram=(self.currentProgram+1)%len(self.programs)
        self.remainingTimeout=self.DEFAULT_TIMEOUT

        if (not self.isDisplayingProgram):
            self.displayCurrentProgram()


    def displayCurrentProgram(self):
        logging.debug('Displaying current program...')
        self.isDisplayingProgram=True
        while self.remainingTimeout > 0:
            self.display.displayProgramSelection(self.programs, self.currentProgram, self.remainingTimeout)
            time.sleep(1)
            self.remainingTimeout-=1
        self.isDisplayingProgram=False
        self.storeLastUsedProgram(self.currentProgram)
        self.station.setParameters(self.programs[self.currentProgram].parameters)
        logging.debug('Displaying current program done')


    def loadLastUsedProgramOrDefault(self):
        file_exists = exists(self.PROGRAM_FILE)
        default=0
        if (file_exists):
            try:
                file = open(self.PROGRAM_FILE, "r")
                p = file.readline()
                file.close()
                return int(p)
            except:
                return default
        else:
            return default

    def storeLastUsedProgram(self, program):
        file = open(self.PROGRAM_FILE, "w")
        file.writelines(program)
        file.close()


