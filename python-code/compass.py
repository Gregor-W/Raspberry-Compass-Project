import setup_display
import setup_sensor
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import multiprocessing as mp
import time

display_refreshrate = 10.0
sensor_refreshrate = 25.0

#print("poll intervall: %d" % setup_sensor.poll_interval)

heading = mp.Value("f", 0)
roll = mp.Value("f", 0)
pitch = mp.Value("f", 0)

def sensor(sem, heading, roll, pitch):
    print("Sensor")
    # timers
    t_damp = time.time()
    t_fail = time.time()
    t_fail_timer = 0.0
    
    faster = 0
    while True:
        hack = time.time()
    
        if (hack - t_damp) > 5.0:
            if (hack - t_fail) > 1.0:
                setup_sensor.reset()
                t_fail_timer += 1
                t_fail = hack
                print("Error: cound not read sensor")

        if setup_sensor.getSensorData():
            t_fail_timer = 0.0
            
            
            #if (hack - t_damp) > 1.0/sensor_refreshrate:
            (l_heading, l_roll, l_pitch) = setup_sensor.convertSensorData()
            with sem:
                heading.value = l_heading
                roll.value = l_roll
                pitch.value = l_pitch
            t_damp = hack
            #else:
            #    faster += 1
            time.sleep(setup_sensor.poll_interval*1.0/50.0)

def display(sem, heading, roll, pitch):

    font = ImageFont.truetype("OpenSans-Regular.ttf")
    background = Image.new("RGB", (setup_display.WIDTH, setup_display.HEIGHT), (0,0,0))
    setup_display.DISPLAY.display(background)
    
    
    print("Display")
    while True:
        hack = time.time()
        
        #image = Image.open("/home/pi/Raspberry-Compass-Project/justworks.jpg")
        #image = image.resize((setup_display.WIDTH, setup_display.HEIGHT), Image.ANTIALIAS)
        #setup_display.DISPLAY.clear((0,0,0))
        #draw = setup_display.DISPLAY.draw()
        
        #small_image = Image.new("RGB", (50, 50), (0,0,0))
        #draw = ImageDraw.Draw(small_image)
        
        image = Image.new("RGB", (setup_display.WIDTH, setup_display.HEIGHT), (0,0,0))
        draw = ImageDraw.Draw(image)
        
        with sem:
            l_heading = heading.value
            l_roll = roll.value
            l_pitch = pitch.value
        
        draw.text((10, 10), "H:" + str(l_heading), font=font)
        draw.text((10, 20), "R:" + str(l_roll), font=font)
        draw.text((10, 30), "P:" + str(l_pitch), font=font)
        
        setup_display.DISPLAY.display(image)
        
        #setup_display.DISPLAY.display(small_image, (10, 10 , 59, 59))
        #print("Heading: %d, Roll: %d, Pitch: %d" % (l_heading, l_roll, l_pitch))
        
        wait_time = 1.0/display_refreshrate - (time.time() - hack)
        if wait_time > 0:
            time.sleep(wait_time)
        else:
            print("Display refreshrate to fast: %f" % wait_time)



sem = mp.Lock()
p_display = mp.Process(target=display, args=(sem, heading, roll, pitch))
p_sensor = mp.Process(target=sensor, args=(sem, heading, roll, pitch))
p_display.start()
p_sensor.start()
