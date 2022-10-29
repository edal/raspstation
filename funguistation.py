import random
import time
from time import sleep

import Adafruit_DHT
from RPLCD import i2c

## CONFIG

TEMP_PIN=23 # BOARD16

# LCD
lcdmode = 'i2c'
cols = 20
rows = 4
charmap = 'A00'
i2c_expander = 'PCF8574'

# Generally 27 is the address;Find yours using: i2cdetect -y 1
address = 0x27
port = 1 # 0 on an older Raspberry Pi

# Initialise the LCD
lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap,
                  cols=cols, rows=rows)

## Custom characters
HAPPY=chr(0)
TEMP=chr(1)
DROP=chr(2)
UP=chr(3)
DOWN=chr(4)
CELSIUS=chr(5)
HEART=chr(6)


happy = (
     0b00000,
     0b01010,
     0b01010,
     0b00000,
     0b10001,
     0b10001,
     0b01110,
     0b00000,
 )
lcd.create_char(0, happy)
lcd.write_string('\x00')
temp = (
0b00100,
0b01010,
0b01010,
0b01110,
0b01110,
0b11111,
0b11111,
0b01110,
)
lcd.create_char(1, temp)
drop = (
0b00100,
0b00100,
0b01010,
0b01010,
0b10001,
0b10001,
0b10001,
0b01110,
)
lcd.create_char(2, drop)

up = (
	0b00000,
	0b00000,
	0b00100,
	0b01110,
	0b11111,
	0b00000,
	0b00000,
	0b00000
)
lcd.create_char(3, up)

down = (
	0b00000,
	0b00000,
	0b00000,
	0b11111,
	0b01110,
	0b00100,
	0b00000,
	0b00000
)
lcd.create_char(4, down)

celsius = (
    0b00000,
	0b00100,
	0b01010,
	0b00100,
	0b00000,
	0b00000,
	0b00000,
	0b00000
)
lcd.create_char(5, celsius)

heart = (
    0b00000,
	0b01010,
	0b11111,
	0b11111,
	0b01110,
	0b00100,
	0b00000,
	0b00000
)
lcd.create_char(6, heart)
####
prevTemp=0
prevHum=0
def printStatus(temp, humidity):
    global prevTemp
    global prevHum
    t = '{:0.1f}'.format(temp)
    h = '{:.0f}'.format(humidity)
    tempChar='='
    if (temp > prevTemp):
        tempChar=UP
    else:
        tempChar=DOWN

    humiChar='='
    if (humidity > prevHum):
        humiChar=UP
    else:
        humiChar=DOWN

    # Write a string on first line and move to next line
    lcd.clear()
    lcd.write_string(HEART + '  Funguistation ' + HAPPY + ' ' + HEART)
    #lcd.crlf()
    lcd.cursor_pos = (2, 0)
    lcd.write_string(' ' + TEMP + ' ' + t + CELSIUS + tempChar)
    lcd.write_string('    ')
    lcd.write_string(DROP + ' ' + h + '%' + humiChar)
    prevTemp=temp
    prevHum=humidity

# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor=Adafruit_DHT.DHT11


def loop():
    # Use read_retry method. This will retry up to 15 times to
    # get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, TEMP_PIN)

    # Reading the DHT11 is very sensitive to timings and occasionally
    # the Pi might fail to get a valid reading. So check if readings are valid.
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}ºC  Humidity={1:0.1f}%'.format(temperature, humidity))
        printStatus(temperature, humidity)
    else:
        print('Failed to get reading. Try again!')

try:
    while True:
        loop()
except KeyboardInterrupt:
    pass
finally:
    print('Exiting')
