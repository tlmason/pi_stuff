#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
import picamera
import os

"""
    This script is used to monitor my desk when I'm not here. People have
    been using my space while I'm gone and leaving their trash, crumbs,
    clothing, and crumbs all over.

    This script uses the PIR Motion Sensor, and the PiCamera to snap photos
    when someone comes into my space.

    Next step: Turn into an interactive loop
    
"""

### Step 0: Initialize

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Create folder to store photos
foldername = time.strftime('%Y%m%d') # Create a folder for the day
if not os.path.exists(foldername):
    os.makedirs(foldername)
    
### Step 1: Set up the camera ###
camera = picamera.PiCamera()

### Step 2: Detect Motion ###
pirmd = 4

GPIO.setup(pirmd, GPIO.IN)

current = 0
previous = 0

# Loop Forever (Ctrl-c quits)
while True:
    current = GPIO.input(pirmd)

    # Decide if the detector was triggered.
    if current == 1 and previous == 0:
        # The motion detector has been triggered!
        previous = current
    elif current == 0 and previous == 1:
        # The motion detector is reset. 
        previous = current

    # If it's triggered, take one photo a second for 5 seconds.
    while current == 1 and previous == 1:
        take_photos(camera)
        
    # wait for 10 ms between motion sensor polling
    time.sleep(0.01)
    
### Step 3: Take Photos ###

def take_photos(cam):
    i = 0
    while i < 5:
        filename = foldername+time.strftime('%Y%m%d %H%M%S')+".jpg"
        cam.capture(filename)
        time.sleep(1.0)

### Step 4: Email them to Box ###

def send_photos_box(folder):
    
