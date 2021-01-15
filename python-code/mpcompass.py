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

# display and plot refreshrate
display_refreshrate = 10.0
plot_refreshrate  = 10.0
#######


# semaphores
heading = mp.Value("f", 0)
roll = mp.Value("f", 0)
pitch = mp.Value("f", 0)

# function for mp, reads sensor values
def sensor(sem, heading, roll, pitch):
    print("started Sensor")
    # timers
    t_damp = time.time()
    t_fail = time.time()
    t_fail_timer = 0.0

    while True:
        hack = time.time()
        
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
            
            (l_heading, l_roll, l_pitch) = setup_sensor.convertSensorData()
            
            # write to semaphore
            with sem:
                heading.value = l_heading
                roll.value = l_roll
                pitch.value = l_pitch
                
            t_damp = hack
            
            # sensor poll rate, might need to be adjusted
            time.sleep(setup_sensor.poll_interval*1.0/50.0)

# function for mp, displays values
def display(sem, heading, roll, pitch):
    print("started Display")
    while True:
        hack = time.time()
        
        # get values from semaphore
        with sem:
            l_heading = heading.value
            l_roll = roll.value
            l_pitch = pitch.value
        
        # display
        if SIMPLEDISLAY:
            setup_display.display(l_heading, l_roll, l_pitch)
        else:
            setup_display.fancy_display(l_heading, l_roll, l_pitch)
        
        # print values to console
        #print("Heading: %d, Roll: %d, Pitch: %d" % (l_heading, l_roll, l_pitch))
        
        # calc time left for refreshrate
        wait_time = 1.0/display_refreshrate - (time.time() - hack)
        if wait_time > 0:
            time.sleep(wait_time)
        else:
            print("Warning: display refreshrate was not reached: %.3f" % wait_time)


# function for mp, writes to file
def write(sem, heading, roll, pitch):
    print("started Write to File")
    outfile = open("/home/pi/plot.txt", 'w')
    
    while True:
        hack = time.time()
        
        # get values from semaphore
        with sem:
            l_heading = heading.value
            l_roll = roll.value
            l_pitch = pitch.value
        
        # write
        outfile.write("{l_heading}, {l_roll}, {l_pitch}, {hack}\n".format(**locals()))
        
        wait_time = 1.0/plot_refreshrate - (time.time() - hack)
        if wait_time > 0:
            time.sleep(wait_time)
        else:
            print("Warning: write refreshrate was not reached: %f" % wait_time)


sem = mp.Lock()
# create mp threads
p_display = mp.Process(target=display, args=(sem, heading, roll, pitch))
p_sensor = mp.Process(target=sensor, args=(sem, heading, roll, pitch))
p_write = mp.Process(target=write, args=(sem, heading, roll, pitch))

# start mp threads
p_sensor.start()
if WRITETOFILE:
    p_write.start()
if DISPLAY:
    p_display.start()