import cv2
import numpy as np
import math
import time
import sys
import threading
from networktables import NetworkTables

#these won't be used in this program, but I'm keeping them here in case I change my mind.
imageCounter=10
maxSeconds=120
delaySeconds=10

imageHeight=480
imageWidth=640
cameraFOV=45

F=894 #focal length pixels
robotAddress="10.2.47.2"  #The address of the network tables server.  Usually the robot
logFileName="/home/pi/testpics/startGSLog.txt"
logfile=open(logFileName,"a+")

c3x1=316
c3y1=247
c3x2=409
c3y2=342

d5x1=62
d5y1=327
d5x2=118
d5y2=377

d6x1=130
d6y1=352
d6x2=171
d6y2=393

d10x1=200
d10y1=394
d10x2=222
d10y2=416

c9x1=311
c9y1=395
c9x2=338
c9y2=421

b7x1=469
b7y1=382
b7x2=503
b7y2=419

b8x1=448
b8y1=396
b8x2=477
b8y2=424

beginning=time.time();

def gametime():
    return time.time()-beginning

logfile.write("New log initiated "+str(gametime())+"\n")

cond=threading.Condition()
notified = [False]

   


#yellow
lowColor=np.array([19,85,140])
highColor=np.array([42,230,255])


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

logfile.write("Detected robot "+str(gametime())+"\n")

#capture 50 frames.  This "warms up" the camera (automatic adjustments
cap = cv2.VideoCapture(0)
if cap.isOpened():
   for i in range(1,50): 
      ret, frame = cap.read()
logfile.write("Camera initialized "+str(gametime())+"\n")
cv2.imwrite("Start_GS.png",frame)
imghls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
mask=cv2.inRange(imghls,lowColor,highColor)
cv2.imwrite("Start_GS_mask.png",mask)

def requiredOnes(x1,y1,x2,y2):
    pixelArea=(x2-x1)*(y2-y1)
    return 0.2*pixelArea


imageCount=0
while (True):
    ret,inimg=cap.read()
    imghls = cv2.cvtColor(inimg, cv2.COLOR_BGR2HLS)
    mask=cv2.inRange(imghls,lowColor,highColor)

    roi=mask[c3y1:c3y2,c3x1:c3x2]
    ones=cv2.countNonZero(roi)
    sd.putBoolean("C3",ones>requiredOnes(c3x1,c3y1,c3x2,c3y2))
    if (imageCount==0):
        logfile.write("C3 "+str(ones))
     
    roi=mask[d5y1:d5y2,d5x1:d5x2]
    ones=cv2.countNonZero(roi)
    sd.putBoolean("d5",ones>requiredOnes(d5x1,d5y1,d5x2,d5y2))
    if (imageCount==0):
        logfile.write("d5 "+str(ones))
        
    roi=mask[d6y1:d6y2,d6x1:d6x2]
    ones=cv2.countNonZero(roi)
    sd.putBoolean("d6",ones>requiredOnes(d6x1,d6y1,d6x2,d6y2))
    if (imageCount==0):
        logfile.write("d6 "+str(ones))
        
    roi=mask[d10y1:d10y2,d10x1:d10x2]
    ones=cv2.countNonZero(roi)
    sd.putBoolean("d10",ones>requiredOnes(d10x1,d10y1,d10x2,d10y2))
    if (imageCount==0):
        logfile.write("d10 "+str(ones))
        
    roi=mask[c9y1:c9y2,c9x1:c9x2]
    ones=cv2.countNonZero(roi)
    sd.putBoolean("c9",ones>requiredOnes(c9x1,c9y1,c9x2,c9y2))
    if (imageCount==0):
        logfile.write("c9 "+str(ones))
        
    roi=mask[b7y1:b7y2,b7x1:b7x2]
    ones=cv2.countNonZero(roi)
    sd.putBoolean("b7",ones>requiredOnes(b7x1,b7y1,b7x2,b7y2))
    if (imageCount==0):
        logfile.write("b7 "+str(ones))
        
    roi=mask[b8y1:b8y2,b8x1:b8x2]
    ones=cv2.countNonZero(roi)
    sd.putBoolean("b8",ones>requiredOnes(b8x1,b8y1,b8x2,b8y2))
    if (imageCount==0):
        logfile.write("b8 "+str(ones))
        
        
    if (imageCount==0):
        logfile.close()
        
    
    imageCount+=1
    sd.putNumber("imageCount",imageCount)

cap.release()



