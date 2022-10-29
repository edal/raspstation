# Install adafruit python to control DHT11 temp+humidity sensor
#git clone https://github.com/adafruit/Adafruit_Python_DHT.git
#cd Adafruit_Python_DHT
sudo apt-get update
sudo apt-get install python3-pip
sudo python3 -m pip install --upgrade pip setuptools wheel

sudo pip3 install Adafruit_DHT



# Ensure I2C is active
# sudo raspi-config
# Interefacing / I2C

sudo apt-get install i2c-tools
sudo echo i2c-bcm2708 >> /etc/modules
sudo echo i2c-dev >> /etc/modules

