import cv2
import numpy as np
import math
import time
import sys


imageCounter=10
maxSeconds=120
delaySeconds=10

imageHeight=480
imageWidth=640
cameraFOV=45

#contour filters
MIN_VERTEX_COUNT=50  #lots of points, because there are no straight edges
MIN_AREA=1000
MAX_RATIO=2
erosionKernel=np.ones((9,9),np.uint8)


#yellow
lowColor=np.array([15,80,130])
highColor=np.array([40,255,255])


firstTime=True    

if True:
    startCapture=time.time()
    now=time.time()
    while(firstTime):
        firstTime=False;
        imageCounter+=1
        print(str(imageCounter))
        savefilename="/home/pi/junk/saveimage"+str(imageCounter)+".png"
        processedfilename="/home/pi/junk/processedimagej"+str(imageCounter)+".png"
        maskname="/home/pi/junk/maskj"+str(imageCounter)+".png"
        inimg=cv2.imread(savefilename)

        flipped=cv2.flip(inimg,0) # flip about the x axis
        #cv2.imwrite(savefilename,flipped)
        cv2.imshow('in',flipped)
        
        #trim the image.
        
        #cropped=flipped[imageHeight/2:imageHeight-1,0:imageWidth-1]
        cropped=flipped
        cv2.imshow('cropped',cropped)
        
        
        #try it without blurring first
        #blurred=cv2.medianBlur(inimg,7)
        imghls = cv2.cvtColor(cropped, cv2.COLOR_BGR2HLS)
        cv2.imshow('imghls',imghls)
        mask=cv2.inRange(imghls,lowColor,highColor)
        erosion=cv2.erode(mask,erosionKernel,iterations = 1)
        mask=cv2.dilate(erosion,erosionKernel,iterations = 1)
        cv2.imshow('mask',mask)
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
        index=-1
        ballindex=-1
        if (len(contours)>0):
            for c in contours:
                index+=1
                if (len(c)<MIN_VERTEX_COUNT):
                    continue
                cArea=cv2.contourArea(c)
                if (cArea<MIN_AREA) or (cArea<=biggestContourArea):
                    continue
                x,y,w,h=cv2.boundingRect(c)
                ratio=(float)(w)/h
                minRatio=(float)(1)/MAX_RATIO
                if (ratio<minRatio) or (ratio>MAX_RATIO):
                    continue;
                #if you get to here, you are g olden
                biggestContourArea=cArea
                biggestContour=c
                ballfound=True
                
                xcenter=x+w/2-imageWidth/2
                ballTheta=cameraFOV*xcenter/(imageWidth/2)
                ballindex=index
                print('x= '+str(x))
                print(xcenter)
                print(ballTheta)
                
                
                
        
        #find the largest contour that fits that description
        #find the x position
        #calculate the angle
        #write the angle to the smartdashboard
        #also write boolean "found" as true or false, depending on whether any contour matched

        #sd.putBoolean("Ball Found",ballfound)
        #sd.putNumber("Ball Yaw",ballTheta)
        if (ballindex!=-1):
            cv2.drawContours(cropped,contours,ballindex,(0,255,0),3)
        cv2.imwrite(processedfilename,cropped)
        cv2.imshow('ball',cropped)
        while(now-startCapture<maxSeconds):
             now=time.time()
             time.sleep(1)
        
#cap.release()
cv2.destroyAllWindows()
sys.exit()





