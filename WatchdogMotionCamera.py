#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
import picamera
import os, inspect, zipfile, sys

""" Take Two

    This script is used to monitor my desk when I'm not here. People have
    been using my space while I'm gone and leaving their trash, crumbs,
    clothing, and crumbs all over.

    This script uses the PIR Motion Sensor, and the PiCamera to snap photos
    when someone comes into my space.

    It initiates a watchdog on the photos folder to email any new file to a
    folder on Box.

"""
# Create a folder for the day, if one does not exist.
folder_name = time.strftime('%Y%m%d') # Create a folder for the day
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Start watchdog to watch this folder for new files.
#### If there's a new file, send it to the box folder.

