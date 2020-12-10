# Commands

# SENSOR
## Installation:
Von hier übernommen:
https://kingtidesailing.blogspot.com/2016/02/how-to-setup-mpu-9250-on-raspberry-pi_25.html
Programme:
```
sudo apt-get install i2c-tools
sudo apt-get install cmake
sudo apt-get install octave
```
I2C anmachen mit:
```
sudo raspi-config
```
I2C test:
```
sudo i2cdetect -y 1
```
RTIMULib Bib:
```
cd ~
git clone https://github.com/RTIMULib/RTIMULib2
cd RTIMULib2/Linux/RTIMULibCal
make -j4
sudo make install
```
## Calibrate Sensor:
```
cd ~/RTIMULib2/RTEllipsoidFit/
RTIMULibCal
```
Config Datei kopieren:
```
cp ~/RTIMULib2/RTEllipsoidFit/RTIMULib.ini ~/Raspberry-Compass-Project
```
## Test:
```
python imutest.py
```
## SampleRate
```
/boot/config.txt
dtparam=i2c1_baudrate=400000

RTIMULib.ini
MPU9250GyroAccelSampleRate=5
MPU9250CompassSampleRate=1
```





# DISPLAY
https://jakew.me/2018/01/19/st7735-pi/

## Installation:
SPI anmachen mit:
```
sudo raspi-config
```
Python Bibliotheken installieren:
```
pip install Pillow
pip install Adafruit_GPIO
pip install RPi.GPIO
cd ~
git clone https://github.com/cskau/Python_ST7735
cd Python_ST7735
sudo python setup.py install
cd ..
```
## Code:
python code von hier:

https://jakew.me/2018/01/19/st7735-pi/

oder benutze testdisplay.py, dann kann ein Bild im gleichen Ordner wie das Skript angezeigt werden

Anpassen von DC = ... und RST = ...
(DC ist bei uns A0, RST ist Reset)

So kann man es aufrufen, ist dann alles in python2:
```
python testdisplay.py
```
