import setup_display
import setup_sensor

import time

display_refreshrate = 60

print("poll intervall: %d" % setup_sensor.poll_interval)

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
        
        # every .05 seconds
        if (hack - t_damp) > 1/display_refreshrate:
            (heading, roll, pitch) = setup_sensor.convertSensorData()
            
            t_damp = hack
            
        # every 1 second:
        if (hack - t_print) > 1:
            print("Heading: %d, Roll: %d, Pitch: %d" % (heading, roll, pitch))
            t_print = hack

        time.sleep(setup_sensor.poll_interval/1000.0)
