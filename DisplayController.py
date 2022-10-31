import logging
import time

from RPLCD import CharLCD, i2c

from StationParameters import StationParameters
from StationStatus import StationStatus


class DisplayController:
    # Internal state
    lcd: i2c.CharLCD

    status: StationStatus = None
    previousStatus: StationStatus = None

    clearedSplash=False


    def __init__(self):
        logging.debug('DisplayController init')
        # Initialise the LCD
        lcdmode = 'i2c'
        cols = 20
        rows = 4
        charmap = 'A02'
        i2c_expander = 'PCF8574'
        address = 0x27
        port = 1
        self.lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap, cols=cols, rows=rows)

        self.__defineCustomCharacters()
        self.__splashScreen()

    # Custom animation to serve as splash screen
    def __splashScreen(self):
        delay=0.2
        self.lcd.clear()
        for i in range(10):
            self.lcd.cursor_pos = (0, i)
            self.lcd.write_string(HEART)
            self.lcd.cursor_pos = (0, 19-i)
            self.lcd.write_string(HEART)
            time.sleep(delay)
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(HEART + '   Fungistation   ' + HEART)

    # Method to show the provided status
    def syncDisplay(self, status: StationStatus, parameters: StationParameters):
        t = '{:0.1f}'.format(status.temperature)
        h = '{:.0f}'.format(status.humidity)

        if (self.previousStatus is None):
            self.previousStatus = status

        tempChar='='
        if (status.temperature == self.previousStatus.temperature):
            tempChar='='
        elif (status.temperature > self.previousStatus.temperature):
            tempChar=UP
        else:
            tempChar=DOWN

        humiChar='='
        if (status.humidity == self.previousStatus.humidity):
            humiChar='='
        elif (status.humidity > self.previousStatus.humidity):
            humiChar=UP
        else:
            humiChar=DOWN

        if (not self.clearedSplash):
            self.lcd.clear()
            self.clearedSplash=True

        if (parameters.MIN_TEMPERATURE <= status.temperature and status.temperature <= parameters.MAX_TEMPERATURE ):
            FACE=HAPPY
        else:
            FACE=SAD

        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(HEART + '   Fungistation ' + FACE + ' ' + HEART)
        self.lcd.cursor_pos = (2, 0)
        self.lcd.write_string(' ' + TEMP + ' ' + t + CELSIUS + tempChar)
        self.lcd.write_string('    ')
        self.lcd.write_string(DROP + ' ' + h + '%' + humiChar)

        self.prevStatus = status


    # LCD allows to store 8 cutsom characters. Let's define there
    def __defineCustomCharacters(self):
        global HAPPY,TEMP,DROP,UP, DOWN,CELSIUS,HEART,SAD

        HAPPY_INDEX=0
        HAPPY=chr(HAPPY_INDEX)
        TEMP_INDEX=1
        TEMP=chr(TEMP_INDEX)
        DROP_INDEX=2
        DROP=chr(DROP_INDEX)
        UP_INDEX=3
        UP=chr(UP_INDEX)
        DOWN_INDEX=4
        DOWN=chr(DOWN_INDEX)
        CELSIUS_INDEX=5
        CELSIUS=chr(CELSIUS_INDEX)
        HEART_INDEX=6
        HEART=chr(HEART_INDEX)
        SAD_INDEX=7
        SAD=chr(SAD_INDEX)

        # Define custom chars to print in LCD
        happy = (0b00000,0b01010,0b01010,0b00000,0b10001,0b10001,0b01110,0b00000)
        self.lcd.create_char(HAPPY_INDEX, happy)
        temp = (0b00100,0b01010,0b01010,0b01110,0b01110,0b11111,0b11111,0b01110)
        self.lcd.create_char(TEMP_INDEX, temp)
        drop = (0b00100,0b00100,0b01010,0b01010,0b10001,0b10001,0b10001,0b01110)
        self.lcd.create_char(DROP_INDEX, drop)
        up = (	0b00000,	0b00000,	0b00100,	0b01110,	0b11111,	0b00000,	0b00000,	0b00000)
        self.lcd.create_char(UP_INDEX, up)
        down = (	0b00000,	0b00000,	0b00000,	0b11111,	0b01110,	0b00100,	0b00000,	0b00000)
        self.lcd.create_char(DOWN_INDEX, down)
        celsius = (    0b00000,	0b00100,	0b01010,	0b00100,	0b00000,	0b00000,	0b00000,	0b00000)
        self.lcd.create_char(CELSIUS_INDEX, celsius)
        heart = (    0b00000,	0b01010,	0b11111,	0b11111,	0b01110,	0b00100,	0b00000,	0b00000)
        self.lcd.create_char(HEART_INDEX, heart)
        sad = (0b00000,	0b01010,0b01010,0b00000,0b01110,0b10001,0b10001,0b00000)
        self.lcd.create_char(SAD_INDEX, sad)
