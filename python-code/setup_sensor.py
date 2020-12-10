import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import math
import operator
import os

DEBUG = True

SETTINGS_FILE = "RTIMULib"
s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

# offsets
yawoff = 0.0
pitchoff = 0.0
rolloff = 0.0

# timers
t_print = time.time()
t_damp = time.time()
t_fail = time.time()
t_fail_timer = 0.0
t_shutdown = 0

if (not imu.IMUInit()):
    print("Error: IMUInit failed")    

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()

# data variables
roll = 0.0
pitch = 0.0
yaw = 0.0
heading = 0.0
rollrate = 0.0
pitchrate = 0.0
yawrate = 0.0

# magnetic deviation
magnetic_deviation = -14


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
        fusionPose = data["fusionPose"]
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
    roll = round(math.degrees(fusionPose[0]) - rolloff, 1)
    pitch = round(math.degrees(fusionPose[1]) - pitchoff, 1)
    yaw = round(math.degrees(fusionPose[2])- yawoff, 1)
    rollrate = round(math.degrees(Gyro[0]), 1)
    pitchrate = round(math.degrees(Gyro[1]), 1)
    yawrate = round(math.degrees(Gyro[2]), 1)
    if yaw < 0.1:
        yaw = yaw + 360
    if yaw > 360:
        yaw = yaw - 360

    # Dampening functions
    roll_total = roll_total - roll_run[t_one]
    roll_run[t_one] = roll
    roll_total = roll_total + roll_run[t_one]
    roll = round(roll_total / 10, 1)
    heading_cos_total = heading_cos_total - heading_cos_run[t_three]
    heading_sin_total = heading_sin_total - heading_sin_run[t_three]
    heading_cos_run[t_three] = math.cos(math.radians(yaw))
    heading_sin_run[t_three] = math.sin(math.radians(yaw))
    heading_cos_total = heading_cos_total + heading_cos_run[t_three]
    heading_sin_total = heading_sin_total + heading_sin_run[t_three]
    yaw = round(math.degrees(math.atan2(heading_sin_total/30,heading_cos_total/30)),1)
    if yaw < 0.1:
        yaw = yaw + 360.0

    # yaw is magnetic heading, convert to true heading
    heading = yaw - magnetic_deviation
    if heading < 0.1:
        heading = heading + 360
    if heading > 360:
        heading = heading - 360
    
    t_one += 1
    if t_one == 10:
        t_one = 0
    t_three += 1
    if t_three == 30:
        t_three = 0
    
    return heading, roll, pitch
