import cv2
import numpy as np
import math
import time
import sys
import threading
from networktables import NetworkTables


imageCounter=10
maxSeconds=120
delaySeconds=10

imageHeight=480
imageWidth=640
cameraFOV=45

F=894 #focal length pixels
robotAddress="10.2.47.2"  #The address of the network tables server.  Usually the robot
logFileName="/home/pi/testpics/runOneLegLog.txt"
auxlogFileName="/home/pi/testpics/auxrunOneLegLog.txt"
auxlogfile=open(auxlogFileName,"a+")
auxlogfile.write("New log initiated "+str(time.time())+"\n")
auxlogfile.close()
logfile=open(logFileName,"a+")
logfile.write("New log initiated "+str(time.time())+"\n")

cond=threading.Condition()
notified = [False]

   


#yellow
lowColor=np.array([19,85,130])
highColor=np.array([42,220,255])


def connectionListener(connected,info):
    print(info,'; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()


NetworkTables.initialize(server="10.2.47.2")
NetworkTables.addConnectionListener(connectionListener,immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()

sd=NetworkTables.getTable('SmartDashboard')
sd.putNumber("Sample Number",247)

logfile.write("Detected robot "+str(time.time())+"\n")

#capture 50 frames.  This "warms up" the camera (automatic adjustments
cap = cv2.VideoCapture(0)
if cap.isOpened():
   for i in range(1,50): 
      ret, frame = cap.read()
logfile.write("Camera initialized "+str(time.time())+"\n")

startrunning=False
while not(startrunning):
    startrunning=sd.getBoolean("InBallChaserLeg",False)

logfile.write("Ball chaser leg detected "+str(time.time())+"\n")
imageCount=0
while (startrunning):
    startrunning=sd.getBoolean("InBallChaserLeg",False)
    ret,inimg=cap.read()
    cv2.imwrite("ballchase"+str(imageCount)+".png",inimg)
    imghls = cv2.cvtColor(inimg, cv2.COLOR_BGR2HLS)
    mask=cv2.inRange(imghls,lowColor,highColor)


    maxones=0
    centercolumn=-1
    for i in range(0,640):
       slice=mask[0:479,i]
       ones=cv2.countNonZero(slice)

       if (ones>maxones):
           maxones=ones
           centercolumn=i
           
    deltaX=centercolumn-320
    thetaX=math.atan(deltaX/F)
    sd.putNumber("thetaX",thetaX)
    sd.putNumber("imageCount",imageCount)
    logfile.write(str(imageCount)+" "+str(thetaX)+" "+str(time.time())+"\n")
    imageCount+=1
    
logfile.write("Leg exited "+str(time.time())+"\n")
logfile.close()
cap.release()


