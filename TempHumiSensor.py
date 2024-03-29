import time

import smbus2

# I2C address of the device
SHT30_DEFAULT_ADDRESS                = 0x44

# SHT30 Command Set
SHT30_MEAS_REP_STRETCH_EN            = 0x2C # Clock stretching enabled
SHT30_MEAS_HIGH_REP_STRETCH_EN        = 0x06 # High repeatability measurement with clock stretching enabled
SHT30_MEAS_MED_REP_STRETCH_EN        = 0x0D # Medium repeatability measurement with clock stretching enabled
SHT30_MEAS_LOW_REP_STRETCH_EN        = 0x10 # Low repeatability measurement with clock stretching enabled
SHT30_MEAS_REP_STRETCH_DS            = 0x24 # Clock stretching disabled
SHT30_MEAS_HIGH_REP_STRETCH_DS        = 0x00 # High repeatability measurement with clock stretching disabled
SHT30_MEAS_MED_REP_STRETCH_DS        = 0x0B # Medium repeatability measurement with clock stretching disabled
SHT30_MEAS_LOW_REP_STRETCH_DS        = 0x16 # Low repeatability measurement with clock stretching disabled
SHT30_CMD_READSTATUS                = 0xF32D # Command to read out the status register
SHT30_CMD_CLEARSTATUS                = 0x3041 # Command to clear the status register
SHT30_CMD_SOFTRESET                    = 0x30A2 # Soft reset command
SHT30_CMD_HEATERENABLE                = 0x306D # Heater enable command
SHT30_CMD_HEATERDISABLE                = 0x3066 # Heater disable command

class SHT30():
    bus: smbus2.SMBus

    def __init__(self):
        # Get I2C bus
        self.bus = smbus2.SMBus(1)

    def write_command(self):
        """Select the temperature & humidity command from the given provided values"""
        COMMAND = [SHT30_MEAS_LOW_REP_STRETCH_EN]
        self.bus.write_i2c_block_data(SHT30_DEFAULT_ADDRESS, SHT30_MEAS_REP_STRETCH_EN, COMMAND)

    def read_data(self):
        self.write_command()
        time.sleep(0.3)
        """Read data back from device address, 6 bytes
        temp MSB, temp LSB, temp CRC, humidity MSB, humidity LSB, humidity CRC"""
        data = self.bus.read_i2c_block_data(SHT30_DEFAULT_ADDRESS, 0, 6)

        # Convert the data
        temp = data[0] * 256 + data[1]
        cTemp = -45 + (175 * temp / 65535.0)
        fTemp = -49 + (315 * temp / 65535.0)
        humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

        return {'c' : cTemp, 'f' : fTemp, 'h' : humidity}

    def print(self):
        self.write_command()
        time.sleep(0.3)
        result = self.read_data()
        print("Relative Humidity : %.2f %%"%(result['h']))
        print("Temperature in Celsius : %.2f C"%(result['c']))
        print("Temperature in Fahrenheit : %.2f F"%(result['f']))
        print(" ************************************* ")
