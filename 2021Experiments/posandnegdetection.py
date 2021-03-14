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

posdir="/home/pi/testpics/pos/"
negdir="/home/pi/testpics/neg/"
posout="/home/pi/testpics/posout/"
negout="/home/pi/testpics/negout/"
ecount=0
stupid=0


def processSampleImage(inimg, outputdir,imageCounter):
        maskname=outputdir+"mask"+str(imageCounter)+".png"
        processedfilename=outputdir+"processedimage"+str(imageCounter)+".png"
        cropped=inimg #cut to the known region of interest.  In this case, full scene
        
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
                print("processing contour "+str(index))
                if (len(c)<MIN_VERTEX_COUNT):
                    print("Rejected due to vertex count")
                    continue
                cArea=cv2.contourArea(c)
                if (cArea<MIN_AREA):
                    print("Rejected due to area")
                    continue
                x,y,w,h=cv2.boundingRect(c)
                ratio=(float)(w)/h
                minRatio=(float)(1)/MAX_RATIO
                if (ratio<minRatio) or (ratio>MAX_RATIO):
                    print("Rejected for squareness")
                    continue;
                
                grayCropped=gray[y:y+h,x:x+w]
                gName=outputdir+"gray_"+str(imageCounter)+"_"+str(index)+".png"
                cv2.imwrite(gName,grayCropped)
                circlesize=min(w/2-2,h/2-2)
                circles = cv2.HoughCircles(grayCropped,cv2.HOUGH_GRADIENT,1,30,param1=55,param2=10,minRadius=2,maxRadius=100)
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

        cv2.imwrite(processedfilename,cropped)
        if (ballindex!=-1):
            cv2.drawContours(cropped,contours,ballindex,(0,0,255),3)
            print("Angle "+str(ballTheta))
            return True
        else:
            return False
        

truePositives=0
falsePositives=0
trueNegatives=0
falseNegatives=0



sampleResult=False
if True:
    for i in range(1,numberPics):
        imageCounter=i
        print(str(imageCounter))
        savefilename=posdir+"saveimage"+str(imageCounter)+".png"
        print(savefilename)
        try:
           inimg=cv2.imread(savefilename)
           if inimg is None:
               stupid+=1
           else:
               print("positive sample "+str(imageCounter))
               sampleResult=processSampleImage(inimg,posout,imageCounter)
               if (sampleResult):
                  truePositives+=1
                  print("True positive")
               else:
                  falseNegatives+=1
                  print("False negative")
        except Exception as e:
            print("Threw pos exception")
            print(e)
            ecount+=1
        
        #savefilename=negdir+"saveimage"+str(imageCounter)+".png"
        #print (savefilename)
        #try:
        #    inimg=cv2.imread(savefilename)
        #    if (inimg is None):
        #         stupid+=1
        #    else:
        #        print("Negative sample "+str(imageCounter))
        #        sampleResult=processSampleImage(inimg,negout,imageCounter)
        #        if (sampleResult):
        #            falsePositives+=1
        #            print("False positive")
        #        else:
        #            trueNegatives+=1
        #            print("True negative")
                
        #except:
        #    ecount+=1
        
           
        
        #trim the image.
        
        #cropped=flipped[imageHeight/2:imageHeight-1,0:imageWidth-1]
print("True positives  "+str(truePositives))
print("True negatives  "+str(trueNegatives))
print("False positives "+str(falsePositives))
print("False negatives "+str(falseNegatives))
    
cv2.destroyAllWindows()
sys.exit()

