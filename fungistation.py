import random
import signal
import time
from csv import writer
from time import sleep

import Adafruit_DHT
import RPi.GPIO as GPIO
from gpiozero import LED, PWMLED
from RPLCD import i2c

# PARAMETERS
MIN_TEMP=23.0
MAX_TEMP=25.0
MIN_HUMIDITY=85.0
MAX_HUMIDITY=98.0

## CONFIG
TEMP_PIN=23 # BOARD16


# Heat
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

RELAIS_1_GPIO = 24
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode

# FANS
# Set the PWM output we are using for the fan
FAN_PWM_PIN = "BOARD12"
FAN_PIN = "BOARD11"
fan_speed = PWMLED(FAN_PWM_PIN)
fan = LED(FAN_PIN)

# LCD
lcdmode = 'i2c'
cols = 20
rows = 4
charmap = 'A02'
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
SAD=chr(7)
HEAT=chr(8)


happy = (0b00000,0b01010,0b01010,0b00000,0b10001,0b10001,0b01110,0b00000)
lcd.create_char(0, happy)
temp = (0b00100,0b01010,0b01010,0b01110,0b01110,0b11111,0b11111,0b01110)
lcd.create_char(1, temp)
drop = (0b00100,0b00100,0b01010,0b01010,0b10001,0b10001,0b10001,0b01110)
lcd.create_char(2, drop)
up = (	0b00000,	0b00000,	0b00100,	0b01110,	0b11111,	0b00000,	0b00000,	0b00000)
lcd.create_char(3, up)
down = (	0b00000,	0b00000,	0b00000,	0b11111,	0b01110,	0b00100,	0b00000,	0b00000)
lcd.create_char(4, down)
celsius = (    0b00000,	0b00100,	0b01010,	0b00100,	0b00000,	0b00000,	0b00000,	0b00000)
lcd.create_char(5, celsius)
heart = (    0b00000,	0b01010,	0b11111,	0b11111,	0b01110,	0b00100,	0b00000,	0b00000)
lcd.create_char(6, heart)
sad = (0b00000,	0b01010,0b01010,0b00000,0b01110,0b10001,0b10001,0b00000)
lcd.create_char(7, sad)

#### Global vars
prevTemp=0
prevHum=0
heatStatus=False
fanStatus=False

splash=True
# Method definition

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def splashScreen():
    delay=0.2
    lcd.clear()
    for i in range(10):
        lcd.cursor_pos = (0, i)
        lcd.write_string(HEART)
        lcd.cursor_pos = (0, 19-i)
        lcd.write_string(HEART)
        time.sleep(delay)
    lcd.cursor_pos = (0, 0)
    lcd.write_string(HEART + '   Fungistation   ' + HEART)




def printStatus(temp, humidity, fan, heat):
    global prevTemp, prevHum, splash

    t = '{:0.1f}'.format(temp)
    h = '{:.0f}'.format(humidity)
    tempChar='='
    if (temp == prevTemp):
        tempChar='='
    elif (temp > prevTemp):
        tempChar=UP
    else:
        tempChar=DOWN

    humiChar='='
    if (humidity == prevHum):
        humiChar='='
    elif (humidity > prevHum):
        humiChar=UP
    else:
        humiChar=DOWN

    if (splash):
        lcd.clear()
        splash=False

    if (MIN_TEMP <= temp and temp <= MAX_TEMP ):
        FACE=HAPPY
    else:
        FACE=SAD

    lcd.cursor_pos = (0, 0)
    lcd.write_string(HEART + '   Fungistation ' + FACE + ' ' + HEART)
    lcd.cursor_pos = (2, 0)
    lcd.write_string(' ' + TEMP + ' ' + t + CELSIUS + tempChar)
    lcd.write_string('    ')
    lcd.write_string(DROP + ' ' + h + '%' + humiChar)
    prevTemp=temp
    prevHum=humidity

# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor=Adafruit_DHT.DHT11

def enableHeat():
    global heatStatus
    GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # out
    heatStatus=True

def disableHeat():
    global heatStatus
    GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on
    heatStatus=False

def enableFan():
    global fanStatus, fan_speed, fan
    fan_speed=1
    fan.on()
    fanStatus=True

def disableFan():
    global fanStatus, fan_speed, fan
    fan_speed=0
    fan.off()
    fanStatus=False

def handle_exit(signum, frame):
    print('Exiting')
    # Switch off backlight
    lcd.backlight_enabled = False
    # Clear the LCD screen
    lcd.close(clear=True)

signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

def loop():
    # Use read_retry method. This will retry up to 15 times to
    # get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, TEMP_PIN)
    # Reading the DHT11 is very sensitive to timings and occasionally
    # the Pi might fail to get a valid reading. So check if readings are valid.
    if humidity is not None and temperature is not None:

        if (temperature < MIN_TEMP):
            enableHeat()
            disableFan()
        elif (temperature >= MIN_TEMP):
            disableHeat()
            disableFan()

        if (temperature > MAX_TEMP):
            enableFan()

        printStatus(temperature, humidity, heatStatus, fanStatus)
        print('Temp={0:0.1f}ºC  Humidity={1:0.1f}% Fan={2} Heat={3}'.format(temperature, humidity, fanStatus, heatStatus))
        # List of strings
        row_contents = [time.strftime('%d/%m/%y %H:%M:%S'),'{:0.1f}'.format(temperature),'{:0.1f}'.format(humidity),fanStatus,heatStatus]
        # Append a list as new line to an old csv file
        append_list_as_row('stats.csv', row_contents)
    else:
        print('Failed to get reading. Try again!')

try:
    splashScreen()
    while True:
        loop()
        time.sleep(10)
except KeyboardInterrupt:
    pass
finally:
    handle_exit()


