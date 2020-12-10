


https://github.com/RTIMULib/RTIMULib2/blob/3d62821fef0f2252c39c14321a68d8cf3a63b9ae/Linux/RTIMULibCal/RTIMULibCal.cpp#L184


###Commands
89SU7R8X

sudo i2cdetect -y 1

RTIMULibCal

### SENSOR ###
###Wie es funktioniert hat:
#1
/boot/config.txt
dtparam=i2c1_baudrate=400000

RTIMULib.ini
MPU9250GyroAccelSampleRate=5
MPU9250CompassSampleRate=1

Python Bind funktioniert nicht mit langsamer rate
Mit alter rate tut es kurz

#2
kabel :P 



### DISPLAY ###
https://jakew.me/2018/01/19/st7735-pi/

## Installation:
#SPI anmachen:

sudo raspi-config

#Python Bibliotheken installieren:
pip install Pillow
pip install Adafruit_GPIO
pip install RPi.GPIO
cd ~
git clone https://github.com/cskau/Python_ST7735
cd Python_ST7735
sudo python setup.py install
cd ..


## Code:
kopier den python code von da:
https://jakew.me/2018/01/19/st7735-pi/
oder nimm mein testdisplay.py, dann kann ein Bild im gleichen Ordner wie das Script angezeigt werden

Anpassen von DC = ... und RST = ...
(DC ist bei uns A0, RST ist Reset)

So kann man es aufrufen, ist dann alles in python2:
python testdisplay.py

