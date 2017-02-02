#!/usr/bin/env python

""" Take Two

    This script is used to monitor my desk when I'm not here. People have
    been using my space while I'm gone and leaving their trash, crumbs,
    clothing, and crumbs all over.

    This script uses the PIR Motion Sensor, and the PiCamera to snap photos
    when someone comes into my space.

    It initiates a watchdog on the photos folder to email any new file to a
    folder on Box.

"""

import time
import RPi.GPIO as GPIO
import picamera
import os, inspect, sys, subprocess


# Create a folder for the day, if one does not exist.
folder_name = time.strftime('%Y%m%d') # Create a folder for the day
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Start watching this folder for new files.
#### If there's a new file, send it to the box folder.

# get full path to folder
folder_path = os.path.dirname(inspect.getfile(inspect.currentframe()))+"/"+folder_name+"/"folder_path = 

subprocess.Popen(["folder_monitor.sh "+folder_path])

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up the camera
camera = picamera.PiCamera()

# Detect Motion
pirmd = 4

GPIO.setup(pirmd, GPIO.IN)

current = 0
previous = 0

# functions here

def take_photos(cam):
    i = 0
    while i < 5:
        file_name = folder_name+"/"+time.strftime('%Y%m%d-%H%M%S')+".jpg"
        cam.capture(file_name)
        print("Photo "+str(i))
        i+=1
        time.sleep(1.0)

# Monitor for motion, take photos, put them in the daily directory, continue
try: 
    # Loop Forever (Ctrl-c quits)
    while True:
        current = GPIO.input(pirmd)

        # Decide if the detector was triggered.
        if current == 1 and previous == 0:
            # The motion detector has been triggered!
            print("motion")
            take_photos(camera)
            previous = current
        elif current == 0 and previous == 1:
            # The motion detector is reset.
            print("reset")
            previous = current
            
        # wait for 10 ms between motion sensor polling
        time.sleep(0.01)
except:
    # When Ctrl-C pressed, send photos, cleanup GPIO
    GPIO.cleanup()
