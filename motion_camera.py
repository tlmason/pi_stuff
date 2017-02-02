#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
import picamera
import os, inspect, zipfile, sys
import gmail_attachment # Personal implementation of python_3_email_with_attachment

"""
    This script is used to monitor my desk when I'm not here. People have
    been using my space while I'm gone and leaving their trash, crumbs,
    clothing, and crumbs all over.

    This script uses the PIR Motion Sensor, and the PiCamera to snap photos
    when someone comes into my space.

    Uses python_3_email_with_attachment.py created by Robert Dempsey on 12/6/14.

    Next step: Turn into an interactive loop.
    
"""

### Step 0: Initialize

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Create folder to store photos
folder_name = time.strftime('%Y%m%d') # Create a folder for the day
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    
### Step 1: Set up the camera ###
camera = picamera.PiCamera()

### Step 2: Detect Motion ###
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

def send_photos_box(folder):
    gmail_attachment.start_sending(folder)

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
        else: # I seem to have a problem with not stopping motion detected state.
            current = 0
            previous = 0
            
        # wait for 10 ms between motion sensor polling
        time.sleep(0.01)
except:
    # When Ctrl-C pressed, send photos, cleanup GPIO
    GPIO.cleanup()
    folder_path = os.path.dirname(inspect.getfile(inspect.currentframe()))+"/"+folder_name+"/"
    send_photos_box(folder_path)


