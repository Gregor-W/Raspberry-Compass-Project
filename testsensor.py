import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math

SETTINGS_FILE = "python-code/RTIMULib"

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

print("IMU Name: " + imu.IMUName())

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded")

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

while True:
  if imu.IMURead():
    x, y, z = imu.getFusionData()
    #print("getFusionData: %f %f %f" % (x,y,z))
    
    data = imu.getIMUData()
    fusionPose = data["fusionPose"]
    compass = data["compass"]
    quaterion = data["quaterion"]
    
    heading = math.degrees(math.atan2(compass[0], compass[1])) 
    
    if heading < 0:
        heading += 360
    
    print("fusion pose r: %.2f p: %.2f y: %.2f, mag only heading: %.2f, quaterion: %.2f, %.2f, %.2f, %.2f" % (math.degrees(fusionPose[0]), 
        math.degrees(fusionPose[1]), math.degrees(fusionPose[2]), heading),
        quaterion[0], quaterion[1], quaterion[2], quaterion[3])
	
	#print("mag only heading: %f" % math.degrees(math.atan2(compass[0], compass[1])))
		
		
    time.sleep(poll_interval*1.0/1000.0)