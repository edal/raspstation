import logging
import time

from RPLCD.i2c import CharLCD

from Program import Program
from StationParameters import StationParameters
from StationStatus import StationStatus


class DisplayController:
    # Internal state
    lcd: CharLCD


    clearedSplash=False


    MAX_TICKS: int = 30
    tick: int = 0


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
        self.lcd = CharLCD(i2c_expander, address, port=port, charmap=charmap, cols=cols, rows=rows)

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
        # Get current tick/cycle
        self.tick=(self.tick+1) % self.MAX_TICKS

        t = '{:0.1f}'.format(status.temperature)
        h = '{:.0f}'.format(status.humidity)

        tempChar=' '
        if (status.previousTemperature is not None):
            if (status.temperature == status.previousTemperature):
                tempChar='='
            elif (status.temperature > status.previousTemperature):
                tempChar=UP
            else:
                tempChar=DOWN

        humiChar=' '
        if (status.previousHumidity is not None):
            if (status.humidity == status.previousHumidity):
                humiChar='='
            elif (status.humidity > status.previousHumidity):
                humiChar=UP
            else:
                humiChar=DOWN

        if (not self.clearedSplash):
            self.lcd.clear()
            self.clearedSplash=True

        if (status.inRange):
            FACE=HAPPY
        else:
            FACE=SAD

        heart_array = [HEART, ' ']
        heart_sprite = heart_array[self.tick%(len(heart_array))]
        title_fungi = heart_sprite + '   Fungistation ' + FACE + ' ' + heart_sprite
        title_program = heart_sprite + '  %d-%d%s %d-%d%% ' % (parameters.MIN_TEMPERATURE, parameters.MAX_TEMPERATURE, CELSIUS, parameters.MIN_HUMIDITY, parameters.MAX_HUMIDITY) + FACE + ' ' + heart_sprite

        if (self.tick%6 < 3):
            title_sprite = title_fungi
        else:
            title_sprite = title_program

        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(title_sprite)
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(' ' + TEMP + ' ' + t + CELSIUS + tempChar)
        self.lcd.write_string('    ')
        self.lcd.write_string(DROP + ' ' + h + '%' + humiChar)

        #self.lcd.cursor_pos = (2, 4)
        #self.lcd.write_string('%d-%d%s %d-%d%%' % (parameters.MIN_TEMPERATURE, parameters.MAX_TEMPERATURE, CELSIUS, parameters.MIN_HUMIDITY, parameters.MAX_HUMIDITY))

        if (status.fanScheduledTicks > 0):
            self.lcd.cursor_pos = (3, 8)
            self.lcd.write_string('%s:%ss' % (FAN, status.fanScheduledTicks))
        else:
            self.lcd.cursor_pos = (3, 8)
            self.lcd.write_string('     ')

        if (status.humidifierScheduledTicks > 0):
            self.lcd.cursor_pos = (3, 15)
            self.lcd.write_string('%s:%ss' % (DROP,status.humidifierScheduledTicks))
        else:
            self.lcd.cursor_pos = (3, 15)
            self.lcd.write_string('    ')

        if (status.isHeatEnabled == True):
            self.lcd.cursor_pos = (3, 1)
            self.lcd.write_string(TEMP + ':ON')
        else:
            self.lcd.cursor_pos = (3, 1)
            self.lcd.write_string('    ')

    def displayProgramSelection(self, programs, programIndex, remainingTimeout: int):
        self.lcd.cursor_pos = (0,0)
        self.lcd.write_string(' Program selection:')
        self.lcd.cursor_pos = (1,0)
        p: Program = programs[programIndex]
        self.lcd.write_string(' %s: %s', p.name, p.description)
        self.lcd.cursor_pos = (2,0)
        self.lcd.write_string(' %d-%d%s %d-%d%% ' % (p.parameters.MIN_TEMPERATURE, p.parameters.MAX_TEMPERATURE, CELSIUS, p.parameters.MIN_HUMIDITY, p.parameters.MAX_HUMIDITY))
        self.lcd.cursor_pos = (3,0)
        self.lcd.write_string('         %ss', remainingTimeout)

    # LCD allows to store 8 cutsom characters. Let's define there
    def __defineCustomCharacters(self):
        global HAPPY,TEMP,DROP,UP, DOWN,CELSIUS,HEART,SAD,FAN

        HAPPY_INDEX=0
        HAPPY=chr(HAPPY_INDEX)
        TEMP_INDEX=1
        TEMP=chr(TEMP_INDEX)
        DROP_INDEX=2
        DROP=chr(DROP_INDEX)
        #UP_INDEX=3
        #UP=chr(UP_INDEX)
        UP='\x5E'
        DOWN_INDEX=4
        DOWN=chr(DOWN_INDEX)
        #CELSIUS_INDEX=5
        #CELSIUS=chr(CELSIUS_INDEX)
        CELSIUS='\xDF'
        FAN='\x2A'
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
        #up = (	0b00000,	0b00000,	0b00100,	0b01110,	0b11111,	0b00000,	0b00000,	0b00000)
        #self.lcd.create_char(UP_INDEX, up)
        down = (0b00000,	0b00000,	0b00000,	0b00000,	0b10001,	0b01010,	0b00100,	0b00000)
        self.lcd.create_char(DOWN_INDEX, down)

        #celsius = (    0b00000,	0b00100,	0b01010,	0b00100,	0b00000,	0b00000,	0b00000,	0b00000)
        #self.lcd.create_char(CELSIUS_INDEX, celsius)
        heart = (    0b00000,	0b01010,	0b11111,	0b11111,	0b01110,	0b00100,	0b00000,	0b00000)
        self.lcd.create_char(HEART_INDEX, heart)
        sad = (0b00000,	0b01010,0b01010,0b00000,0b01110,0b10001,0b10001,0b00000)
        self.lcd.create_char(SAD_INDEX, sad)

    def tearDown(self):
        logging.debug("Tearing down display controller")
        # Switch off backlight
        self.lcd.backlight_enabled = False
        # Clear the LCD screen
        self.lcd.close(clear=True)
