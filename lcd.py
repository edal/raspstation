# Import LCD library
# Import sleep library
import time
from time import sleep

from RPLCD import i2c

# constants to initialise the LCD
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


# Scrolling text
framebuffer = [
    'Funguistation',
    '',
    ]
def write_to_lcd(lcd, framebuffer, num_cols):
    """Write the framebuffer out to the specified LCD."""
    lcd.home()
    for row in framebuffer:
        lcd.write_string(row.ljust(num_cols)[:num_cols])
        lcd.write_string('\r\n')

def loop_string(string, lcd, row, num_cols, delay=0.3):
    padding = ' ' * num_cols
    s = padding + string + padding
    for i in range(len(s) - num_cols + 1):
        framebuffer[row] = s[i:i+num_cols]
        write_to_lcd(lcd, framebuffer, num_cols)
        time.sleep(delay)
####


# Printar hora
lcd.write_string('Time: %s', time.strftime('%H:%M:%S'))

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

# Write a string on first line and move to next line
lcd.clear()
lcd.write_string(HEART + '  Funguistation ' + HAPPY + ' ' + HEART)
#lcd.crlf()
lcd.cursor_pos = (2, 0)
lcd.write_string(' ' + TEMP + ' 24' + CELSIUS + ' ' + UP)
lcd.write_string('    ')
lcd.write_string(DROP + ' 90% ' + DOWN)



sleep(5)
# Switch off backlight
lcd.backlight_enabled = False
# Clear the LCD screen
lcd.close(clear=True)
