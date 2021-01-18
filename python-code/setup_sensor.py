import sys, getopt
sys.path.append('.')
import RTIMU
import os.path
import math
import operator
import os

### options ###
# Rolling average filter
# turn filter on/off
DAMPENING = True
# amount values to be averaged
RA_ROLL = 10 # default 10
RA_HEADING = 10 # default 30

# magnetic deviation
magnetic_deviation = 3

# offsets (enter values when sensor level)
yawoff = 0.0
pitchoff = 0.0
rolloff = 0.0

SETTINGS_FILE = "/home/pi/Raspberry-Compass-Project/python-code/RTIMULib"

# set compass calibration during runtime
COMPASSCALIBRATION = False
######


s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

if (not imu.IMUInit()):
    print("Error: IMUInit failed")    

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)
imu.setCompassCalibrationMode(COMPASSCALIBRATION)
# reset Fusion
imu.resetFusion()

print("IMUGyroBiasValid:")
print(imu.IMUGyroBiasValid())
print("CompassCalibrationValid:")
print(imu.getCompassCalibrationValid())
print("CompassCalibrationEllipsoidValid:")
print(imu.getCompassCalibrationEllipsoidValid())
print("AccelCalibrationValid:")
print(imu.getAccelCalibrationValid())

poll_interval = imu.IMUGetPollInterval()

# data variables
roll = 0.0
pitch = 0.0
yaw = 0.0
heading = 0.0
rollrate = 0.0
pitchrate = 0.0
yawrate = 0.0

# dampening variables
t_one = 0
t_three = 0
roll_total = 0.0
roll_run = [0] * 10
heading_cos_total = 0.0
heading_sin_total = 0.0
heading_cos_run = [0] * 30
heading_sin_run = [0] * 30

data = None
fusionPose = None
Gyro = None

def reset():
    t_one = 0
    t_three = 0
    roll_total = 0.0
    roll_run = [0] * 10
    heading_cos_total = 0.0
    heading_sin_total = 0.0
    heading_cos_run = [0] * 30
    heading_sin_run = [0] * 30

# get Data
def getSensorData():
    global data, fusionPose, Gyro
    if imu.IMURead():
        data = imu.getIMUData()
        fusionPose = data["fusionPose"] #fusionPose, fusionQPose, compass
        if not data["compassValid"]:
            print("Not valid")
        Gyro = data["gyro"]
        return True
    else:
        print("Error: failed to IMURead")
        return False

# convert sensor data to pitch, roll, heading
def convertSensorData():
    global roll_total, roll_run
    global heading_cos_total, heading_sin_total, heading_cos_run, heading_sin_run
    global t_one, t_three
    
    # get RTIMU data
    roll = round(math.degrees(fusionPose[0]) - rolloff, 1)
    pitch = round(math.degrees(fusionPose[1]) - pitchoff, 1)
    yaw = round(math.degrees(fusionPose[2])- yawoff, 1)
    rollrate = round(math.degrees(Gyro[0]), 1)
    pitchrate = round(math.degrees(Gyro[1]), 1)
    yawrate = round(math.degrees(Gyro[2]), 1)
    
    # normalize heading
    if yaw < 0.1:
        yaw = yaw + 360
    if yaw > 360:
        yaw = yaw - 360
    
    if DAMPENING:
        # Dampening functions
        # running average for roll
        roll_total = roll_total - roll_run[t_one]
        roll_run[t_one] = roll
        roll_total = roll_total + roll_run[t_one]
        roll = round(roll_total / RA_ROLL, 1)
        
        # running average for heading
        heading_cos_total = heading_cos_total - heading_cos_run[t_three]
        heading_sin_total = heading_sin_total - heading_sin_run[t_three]
        heading_cos_run[t_three] = math.cos(math.radians(yaw))
        heading_sin_run[t_three] = math.sin(math.radians(yaw))
        heading_cos_total = heading_cos_total + heading_cos_run[t_three]
        heading_sin_total = heading_sin_total + heading_sin_run[t_three]
        yaw = round(math.degrees(math.atan2(heading_sin_total/RA_HEADING,heading_cos_total/RA_HEADING)),1)
        
        # normalize heading
        if yaw < 0.1:
            yaw = yaw + 360.0
        
        # running average helper variables
        t_one += 1
        if t_one == RA_ROLL:
            t_one = 0
        t_three += 1
        if t_three == RA_HEADING:
            t_three = 0

    # yaw is magnetic heading, convert to true heading
    heading = yaw - magnetic_deviation
    if heading < 0.1:
        heading = heading + 360
    if heading > 360:
        heading = heading - 360

    return heading, roll, pitch
