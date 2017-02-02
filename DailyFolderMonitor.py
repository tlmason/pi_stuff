#!/usr/bin/env python

"""
    This file will be called from a bash script to email the contents of a
    folder when the folder has changed.

    Once files are emailed, they will be removed.

"""
import time
from datetime import datetime
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import sys, os, inspect, getopt

def main(argv):
    # Assign Variables
    toaddr = 'Office_.4801ln9e3g967uv4@u.box.com'    # redacted
    me = 'tlmason@tlmason.com' # redacted
    subject = 'Security Camera Photo'
    folder_path = argv[1]

    # List of attachments
    attachments = []
    for file in os.listdir(folder_path):
        attachments.append(folder_path+file)

    # Send each attachment via email
    for file in attachments:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = toaddr
        msg.preamble = "Photo"

        fp = open(file, 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)

        try:
           s = smtplib.SMTP('localhost')
           s.send_message(msg)
           s.quit()
           # Remove the file just sent
        except:
           print ("Error: unable to send email")

"""


try:
   s = smtplib.SMTP('localhost')
   s.send_message(msg)
   s.quit()
except:
   print ("Error: unable to send email")


"""
if __name__ == "__main__":
    # Main Program Goes Here
