import setup_display
import setup_sensor
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


import time

display_refreshrate = 60.0

# timers
t_print = time.time()
t_damp = time.time()
t_fail = time.time()
t_fail_timer = 0.0
t_shutdown = 0

print("poll intervall: %d" % setup_sensor.poll_interval)


image = Image.open("/home/pi/Raspberry-Compass-Project/justworks.jpg")
image = image.resize((setup_display.WIDTH, setup_display.HEIGHT), Image.ANTIALIAS)
draw = ImageDraw.Draw(image)
width, height = image.size

font = ImageFont.load("arial.pil")

setup_display.DISPLAY.display(image)

while True:
    
    hack = time.time()

    # if it's been longer than 5 seconds since last print
    if (hack - t_damp) > 5.0:
      
        if (hack - t_fail) > 1.0:
            setup_sensor.reset()
            t_fail_timer += 1
            t_fail = hack
            print("Error: cound not read sensor")

    if setup_sensor.getSensorData():
        t_fail_timer = 0.0
        
        if (hack - t_damp) > 1.0/display_refreshrate:
            (heading, roll, pitch) = setup_sensor.convertSensorData()
            
            t_damp = hack
            
        # every 1 second:
        if (hack - t_print) > 1:
        
            
            setup_display.DISPLAY.display(image)
            print("Heading: %d, Roll: %d, Pitch: %d" % (heading, roll, pitch))
            t_print = hack

        time.sleep(setup_sensor.poll_interval/100.0)
