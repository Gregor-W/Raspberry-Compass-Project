# Commands

# SENSOR
https://invensense.tdk.com/products/motion-tracking/9-axis/mpu-9250/ 
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
git clone https://github.com/HongshiTan/RTIMULib2
cd RTIMULib2/Linux/RTIMULibCal
make -j4
sudo make install
```
RTIMULib python:
```
cd ~/RTIMULib2/Linux/python/
sudo apt-get install python-dev
python setup.py build
python setup.py install
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
https://www.az-delivery.de/en/products/1-8-zoll-spi-tft-display
## Installation:
https://jakew.me/2018/01/19/st7735-pi/
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
git clone https://github.com/Gregor-W/Python_ST7735.git
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
git clone https://github.com/Gregor-W/Raspberry-Compass-Project.git
python testdisplay.py
```


# Autostart + display fix
https://tutorials-raspberrypi.de/raspberry-pi-autostart-programm-skript/
https://unix.stackexchange.com/questions/57292/how-can-i-make-this-daemon-init-run-as-a-non-root-user
http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/
Add program to autostart
```
cp ~/Raspberry-Compass-Project/compass /etc/init.d/
sudo chmod 755 /etc/init.d/compass
sudo update-rc.d compass defaults
```
To later remove it from autostart:
```
sudo update-rc.d -f  compass remove
```
To stop it anytime:
```
killall python
```

