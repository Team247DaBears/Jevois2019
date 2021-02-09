import cv2
import numpy as np
import math
import time
import sys

imageCounter=0
maxImages=10
maxSeconds=120
delaySeconds=10

#yellow
lowColor=np.array([15,175,100])
highColor=np.array([40,255,255])

startTime=time.time()
now=time.time()
while(now-startTime<delaySeconds):
    now=time.time()
    
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
        print(maskname)
        cv2.imwrite(savefilename,inimg)

        blurred=cv2.medianBlur(inimg,7)
        imghls = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(imghls,lowColor,highColor)
        cv2.imwrite(maskname,mask)


        edges=cv2.Canny(mask,20,200)
        circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,1,30,param1=100,param2=25,minRadius=0,maxRadius=0)

        if circles is not None:
            print("here")
            mask=cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
            circles=np.around(circles)

            circles = np.uint16(circles)
    
            biggestRadius=0
           
    
            for i in circles[0,:]:
                # draw the outer circle
                print("processing")
                if (i[2]>biggestRadius):
                    bigCircle=i
                    biggestRadius=i[2]
            #at his point, we are guaranteed to have a biggest circle
            cv2.circle(inimg,(bigCircle[0],bigCircle[1]),bigCircle[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(inimg,(bigCircle[0],bigCircle[1]),2,(0,0,255),3)



        else:
            print("no circles found")
        cv2.imwrite(processedfilename,inimg)
        now=time.time()
        
cap.release()
cv2.destroyAllWindows()
sys.exit()



