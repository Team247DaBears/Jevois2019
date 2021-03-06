import cv2
import numpy as np
import math
import time
import sys
import threading
from networktables import NetworkTables


imageCounter=0
maxSeconds=120
delaySeconds=30

imageHeight=480
imageWidth=640
cameraFOV=45

#contour filters
MIN_VERTEX_COUNT=50  #lots of points, because there are no straight edges
MIN_AREA=1000
MAX_RATIO=2
erosionKernel=np.ones((9,9),np.uint8)


#yellow
lowColor=np.array([15,100,190])
highColor=np.array([40,200,255])

robotAddress="10.2.47.2"  #The address of the network tables server.  Usually the robot

cond=threading.Condition()
notified = [False]

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

startTime=time.time()
now=time.time()

while(now-startTime<delaySeconds):
    now=time.time()
    
sd.putBoolean("Capturing Photos",True)
cap = cv2.VideoCapture(0)
if cap.isOpened():
    startCapture=time.time()
    while(now-startCapture<maxSeconds):
        imageCounter+=1
        print(str(imageCounter))
        ret, inimg = cap.read()
        savefilename="/home/pi/junk/saveimage"+str(imageCounter)+".png"
        processedfilename="/home/pi/junk/processedimage"+str(imageCounter)+".png"
        maskname="/home/pi/junk/mask"+str(imageCounter)+".png"

        flipped=cv2.flip(inimg,0) # flip about the x axis
        cv2.imwrite(savefilename,flipped)
        
        #trim the image.
        
        #cropped=flipped[imageHeight/2:imageHeight-1,0:imageWidth-1]
        cropped=flipped
        
        #try it without blurring first
        #blurred=cv2.medianBlur(inimg,7)
        imghls = cv2.cvtColor(cropped, cv2.COLOR_BGR2HLS)
        mask=cv2.inRange(imghls,lowColor,highColor)
        erosion=cv2.erode(mask,erosionKernel,iterations = 1)
        mask=cv2.dilate(erosion,erosionKernel,iterations = 1)
        cv2.imwrite(maskname,mask)
        

        # Find contours
        contours,hierarchy=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        ballfound=False;
        ballTheta=-100;
        
        #filter the contours
        # ratio of width<height<2
        # ratio of height-width <2
        # At least 1000 pixels
        # High numbers of points
        biggestContourArea=0
        biggestContour=None
        ballindex=-1
        index=-1
        print("cont "+str(len(contours)))
        if (len(contours)>0):
            for c in contours:
                index+=1
                if (len(c)<MIN_VERTEX_COUNT):
                    continue
                cArea=cv2.contourArea(c)
                if (cArea<MIN_AREA) or(cArea<=biggestContourArea):
                    continue
                x,y,w,h=cv2.boundingRect(c)
                ratio=(float)(w)/h
                minRatio=(float)(1)/MAX_RATIO
                if (ratio<minRatio) or (ratio>MAX_RATIO):
                    continue;
                #if you get to here, you are golden
                biggestContourArea=cArea
                biggestContour=c
                ballfound=True
                xcenter=x+w/2-imageWidth/2
                ballTheta=cameraFOV*xcenter/(imageWidth/2)#should be arctan x/F,
                ballindex=index
                
                
                
                
        
        #find the largest contour that fits that description
        #find the x position
        #calculate the angle
        #write the angle to the smartdashboard
        #also write boolean "found" as true or false, depending on whether any contour matched

        sd.putBoolean("Ball Found",ballfound)
        sd.putNumber("Ball Yaw",ballTheta)
        
        if (ballindex!=-1):
            cv2.drawContours(cropped,contours,ballindex,(0,255,0),3)
            print("Angle "+str(ballTheta))
        cv2.imwrite(processedfilename,cropped)
        now=time.time()
    
sd.putBoolean("Capturing Photos",False)
cap.release()
cv2.destroyAllWindows()
sys.exit()




