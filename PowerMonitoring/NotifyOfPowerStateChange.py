#!/usr/bin/env python3

import os
import time
import datetime
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

loopTimeMinutes = 1
powerFailed=False

# Email info
smsTo = ['phonenumber@msg.fi.google.com','phonenumber@mms.att.net']
emailFrom = '<emailaddress>'
emailUser = '<emailaddress>'
emailPassword = '<password>'

# PV settings
mate3IPAddress = '<ipaddress>'
pvURL = f"http://{mate3IPAddress}/Dev_status.cgi?Port=0"

def getPVDataFromMate3(pvURL):
    retryCounter = 0
    while retryCounter < 5:
        try:
            pvData = requests.get(pvURL)
            pvJSONData = pvData.json()
            return pvJSONData
        except:
            # Try again
            print(f"Unable to retreive PV Data from Mate3...attempt {retryCounter+1}")
            time.sleep(2)
            retryCounter += 1
    else:
        print (f"Repeated attempts to connecto to the Mate3 web server has failed.  Exiting")
        sendEmail(emailUser,emailPassword,emailUser,emailUser,'Error: Mate3 connection failure','Mate 3 is not accessible.  Reboot the Mate3')
        return 'fail'


def sendEmail (user, password, toUser, fromUser, emailSubject, emailBody):
    smtp = "smtp.gmail.com" 
    port = 587
    # This will start our email server
    server = smtplib.SMTP(smtp,port)
    # Starting the server
    server.starttls()
    # Now we need to login
    server.login(user,password)

    # Now we use the MIME module to structure our message.
    msg = MIMEMultipart()
    msg['From'] = fromUser
    msg['To'] = ", ".join(toUser)
    # Make sure you add a new line in the subject
    msg['Subject'] = "%s\n" % emailSubject
    # Make sure you also add new lines to your body
    body = "%s\n" % emailBody
    # and then attach that body furthermore you can also send html content.
    msg.attach(MIMEText(body, 'plain'))

    sms = msg.as_string()

    server.sendmail(user,toUser,sms)

    # lastly quit the server
    server.quit()

while True:
    # Get PV information from Mate3
    print("Get PV data from Mate3...",end='')
    pvJSONData = getPVDataFromMate3(pvURL)

    now = datetime.datetime.now()
    currentTime = now.strftime("%H:%M")
    today=datetime.datetime.today()

    if(pvJSONData == 'fail'):
        print('Failed to get pv date at %s %s' % (today.strftime("%Y/%m/%d"),currentTime))
        continue
    else:
        print('Done at %s %s' % (today.strftime("%Y/%m/%d"),currentTime))
    
    previousPowerFailed=powerFailed
    if((pvJSONData['devstatus']['ports'][0]['VAC1_in_L1']==0) and pvJSONData['devstatus']['ports'][0]['VAC1_in_L2']==0):
        powerFailed=True
        emailSubject = 'Power Outage Detected'
        emailBody = 'Power dropped at %s %s' % (today.strftime("%Y/%m/%d"),currentTime)
    else:
        powerFailed=False
        emailSubject = 'Power Restored'
        emailBody = 'Power has returned at %s %s' % (today.strftime("%Y/%m/%d"),currentTime)

    if previousPowerFailed != powerFailed:
        sendEmail (emailUser,emailPassword,smsTo,emailFrom,emailSubject,emailBody)
        print("%s:%s" % (emailSubject,emailBody))
  
    time.sleep(loopTimeMinutes*60)