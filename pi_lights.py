#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from phue import Bridge

pir_sensor = 4

b = Bridge('10.0.1.15')#keep the quotes when you put the ip
b.connect()
b.get_api()

GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_sensor, GPIO.IN)

previous_state = 0
current_state = 0

try:
    while True:
        # current state = 1 if motion is detected, 0 if none
        current_state = GPIO.input(pir_sensor)
        if current_state == 1 and previous_state == 0:
            print("----------------------\n|Lights currently off|\n|   Motion Detected  |\n|     Turn'em on     |\n----------------------\n\n")
            #assumes you have 3 light bulbs
            b.set_light( [1,2,3], 'on', True)
            previous_state = 1
            t_end = time.time() + 60*10+1 #seconds * num minutes
            #this loop keeps the lights on for X minutes... if motion detected in loop, it extends the amount of time lights are on.
            while time.time() < t_end:
                if(t_end-time.time() > 60):
		    minutes = int((t_end - time.time())/60)
		    seconds = int(t_end-time.time())%60
		    print("Lights will stay on for %s minutes and %s seconds" %(minutes, seconds ))
		else:
		    print("Lights will stay on for %s more seconds" %(int((t_end-time.time()))))
                if((t_end-time.time()) > 39):
                    time.sleep(5)
                else:
                    time.sleep(1)
                current_state = GPIO.input(pir_sensor)
                if current_state == 1:
                    print("Motion Detected - Reset Timer")
                    #reset the timeout if motion detected within time limit
                    t_end = time.time() + 60 * 10 + 1 
        elif current_state == 0 and previous_state == 1:
            print("----------------------\n| Lights currenly on |\n| No Motion Detected |\n|   Turn lights off  |\n----------------------\n\n")
            b.set_light( [1,2,3], 'on', False)
            previous_state = 0
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()

