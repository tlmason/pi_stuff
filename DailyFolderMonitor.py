#!/usr/bin/env python

"""
    This file will be called from a bash script to email the contents of a
    folder when the folder has changed.

    Once files are emailed, they will be removed.

"""

import sys, os, inspect, getopt

def main(argv):
    folder_path = argv[1]

    # List of attachments
    attachments = []
    for file in os.listdir(folder_path):
        attachments.append(folder_path+file)
    
    
if __name__ == "__main__":
    # Main Program Goes Here
