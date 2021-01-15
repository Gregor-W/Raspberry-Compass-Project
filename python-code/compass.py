#!/usr/bin/env python
import setup_display
import setup_sensor
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import multiprocessing as mp
import time
### options ###
# turn write to file on/off
WRITETOFILE = False
# turn display on/off
DISPLAY = True
# select simple or graphic display
SIMPLEDISLAY = True

# compass refreshrate
refreshrate = 10.0
#######


# open file to write
if WRITETOFILE:
    outfile = open("/home/pi/plot.txt", 'w')

# loop for everything
while True:
    hack = time.time()
    
    # timers
    t_damp = time.time()
    t_fail = time.time()
    t_fail_timer = 0.0
    
    # check if sensor didn't work for 5s
    if (hack - t_damp) > 5.0:
        if (hack - t_fail) > 1.0:
            setup_sensor.reset()
            t_fail_timer += 1
            t_fail = hack
            print("Error: cound not read sensor")
    
    # read sensor
    if setup_sensor.getSensorData():
        t_fail_timer = 0.0
        
        (heading, roll, pitch) = setup_sensor.convertSensorData()
        t_damp = hack
        
        if WRITETOFILE:
            outfile.write("{heading}, {roll}, {pitch}, {hack}\n".format(**locals()))
        
        # display new values
        if DISPLAY:
            if SIMPLEDISLAY:
                setup_display.display(heading, roll, pitch)
            else:
                setup_display.fancy_display(heading, roll, pitch)
        
        # print values to console
        #print("Heading: %d, Roll: %d, Pitch: %d" % (heading, roll, pitch))
        
        # calc time left for refreshrate
        wait_time = 1.0/refreshrate - (time.time() - hack)
        if wait_time > 0:
            time.sleep(wait_time)
        else:
            print("Warning: target refreshrate was not reached: %.3f" % wait_time)
        
        