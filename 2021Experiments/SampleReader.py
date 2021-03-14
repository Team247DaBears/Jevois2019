import cv2
import numpy as np
import math
import time
import sys
import threading



imageCounter=0
maxSeconds=120
delaySeconds=30
numberPics=472

imageHeight=480
imageWidth=640
cameraFOV=45

#contour filters
MIN_VERTEX_COUNT=50  #lots of points, because there are no straight edges
MIN_AREA=1000
MAX_RATIO=2
erosionKernel=np.ones((9,9),np.uint8)


#yellow
lowColor=np.array([15,100,170])
highColor=np.array([40,255,255])

robotAddress="10.2.47.2"  #The address of the network tables server.  Usually the robot

cond=threading.Condition()
notified = [False]


if True:
    for i in range(1,numberPics):
        imageCounter=i
        print(str(imageCounter))
        savefilename="/home/pi/testpics/saveimage"+str(imageCounter)+".png"
        processedfilename="/home/pi/testpics/processedimage"+str(imageCounter)+".png"
        maskname="/home/pi/testpics/mask"+str(imageCounter)+".png"
        inimg=cv2.imread(savefilename)
        
        #trim the image.
        
        #cropped=flipped[imageHeight/2:imageHeight-1,0:imageWidth-1]
        cropped=inimg
        
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
            gray=cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY)
            for c in contours:
                index+=1
                if (len(c)<MIN_VERTEX_COUNT):
                    continue
                cArea=cv2.contourArea(c)
                if (cArea<MIN_AREA):
                    continue
                x,y,w,h=cv2.boundingRect(c)
                ratio=(float)(w)/h
                minRatio=(float)(1)/MAX_RATIO
                if (ratio<minRatio) or (ratio>MAX_RATIO):
                    continue;
                
                grayCropped=gray[y:y+h,x:x+w]
                gName="/home/pi/testpics/gray_"+str(imageCounter)+"_"+str(index)+".png"
                cv2.imwrite(gName,grayCropped)
                circles = cv2.HoughCircles(grayCropped,cv2.HOUGH_GRADIENT,1,30,param1=100,param2=25,minRadius=6,maxRadius=100)
                cv2.drawContours(cropped,contours,index,(0,255,0),3)
                if circles is None: 
                    print("No circles")
                    continue
                circles = np.uint16(np.around(circles))

                howmany=0
                for circ in circles[0,:]:
                    if (circ[2]==0):
                        print("deleting a zero radius circle")
                        continue
                    print(str(x)+" "+str(y)+" "+str(w)+" "+str(h)+" "+str(circ[0])+" "+str(circ[1])+" "+str(circ[2])+" ")
                    howmany+=1
                    cv2.circle(cropped,(circ[0]+x,circ[1]+y),circ[2],(255,0,0),2)
                
                    

                print("I found "+str(howmany)+" circles")
                #if you get to here, you are golden
                if (cArea>biggestContourArea):
                    biggestContourArea=cArea
                    biggestContour=c
                    ballfound=True
                    xcenter=x+w/2-imageWidth/2
                    ballTheta=cameraFOV*xcenter/(imageWidth/2)#should be arctan x/F,
                    ballindex=index
                    cv2.drawContours(cropped,contours,ballindex,(0,255,0),3)
                
                
                
                
        
        #find the largest contour that fits that description
        #find the x position
        #calculate the angle
        #write the angle to the smartdashboard
        #also write boolean "found" as true or false, depending on whether any contour matched

        
        if (ballindex!=-1):
            cv2.drawContours(cropped,contours,ballindex,(0,0,255),3)
            print("Angle "+str(ballTheta))
        cv2.imwrite(processedfilename,cropped)
    
cv2.destroyAllWindows()
sys.exit()





