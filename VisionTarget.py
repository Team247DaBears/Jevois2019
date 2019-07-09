import libjevois as jevois
import cv2
import numpy as np
import random
import math

## Detect Vision Targets
#
# Add some description of your module here.
#
# @author Dave
# 
# @videomapping YUYV 320 240 16 YUYV 640 480 16 Dave VisionTarget
# @email x
# @address 123 first street, Los Angeles CA 90012, USA
# @copyright Copyright (C) 2018 by Dave
# @mainurl x
# @supporturl x
# @otherurl x
# @license x
# @distribution Unrestricted
# @restrictions None
# @ingroup modules
class VisionTarget:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("processing timer", 100, jevois.LOG_INFO)
        self.imagecount=1
        self.minimagecount=142
        self.maximagecount=360
        self.currentimagecount=self.minimagecount
        #self.cameraMatrix=np.matrix([[659.0,342],[0,658,250],[0,0,1]])
        #self.distcoeff=np.matrix([0.236,-0.290,-0.00115,-0.00087,-2.4])
        self.currentloopcount=0
        self.maxloopcount=15

        self.cameraMatrix=np.zeros((3,3))
        self.cameraMatrix[0][0]=329.0
        self.cameraMatrix[0][2]=120
        self.cameraMatrix[1][1]=329
        self.cameraMatrix[1][2]=160
        self.cameraMatrix[2][2]=1
        
        self.distcoeff=np.zeros((1,5))
        self.distcoeff[0][0]=0.236
        self.distcoeff[0][1]=-0.290
        self.distcoeff[0][2]=-0.00115
        self.distcoeff[0][3]=-0.00087
        self.distcoeff[0][4]=-2.4
                
        self.currentimagecount=random.randint(1,50001)
        self.datafile=open("targetData.txt","w+")
        self.written=False

    def logstring(self, lstring):
        self.datafile.write(lstring)
        
    def logstringonce(self,lstring):
        if (self.written==False):
            self.datafile.write(lstring)    
    
    def rotationMatrixToEulerAngles(self,R):   #r is the output of Rodrigues, when the input is rvec
       sy=np.sqrt(R[0][0]*R[0][0]+R[1][0]*R[1][0])
       singular=False
       if (sy<0.000001):
           singular=True
       x=0
       y=0
       z=0

       #xyz is roll, yaw, pitch
       if (singular==False):
           x=math.atan2(R[2][1],R[2][2])
           y=math.atan2(-R[2][0],sy)
           z=math.atan2(R[1][0],R[0][0])
       else:
           x=math.atan2(-R[1][2],R[1][1])
           y=math.atan2(-R[2][0],sy)
           z=0
       return y    
        

    def processNoUSB(self, inframe):
        # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR. If you need a
        # grayscale image, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB() and getCvRGBA():
        inimg = inframe.getCvBGR()
        
        imagefilename="practice"+str(self.imagecount)+".png"
        self.imagecount=self.imagecount+1
        
        cv2.imwrite(imagefilename, inimg)            
    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe, outframe):

        
        imagefilename="practice"+str(self.currentimagecount)+".png"
        
      #  inimg = cv2.imread(imagefilename+)
      #  inimg=cv2.imread("practice7354.png")      
        
        inimg=inframe.getCvBGR()
        self.currentimagecount+=1
        cv2.imwrite(imagefilename,inimg)
        inimg=cv2.transpose(inimg)
        inimg=cv2.flip(inimg, 1)

        

        
        lowColor=np.array([53,20,211])
        highColor=np.array([86,255,255])
        imghls = cv2.cvtColor(inimg, cv2.COLOR_BGR2HLS)
      

        mask=cv2.inRange(imghls,lowColor,highColor)
        
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

 #now filter the contours
        
        biggestIndex=-1;
        secondIndex=-1;
        biggestSize=0;

        secondSize=0;
        index=0
        
        backtorgb=cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
        if len(contours)>0:
           for c in contours:
               if cv2.contourArea(c)>biggestSize:
                  secondSize=biggestSize
                  secondIndex=biggestIndex
                  biggestSize=cv2.contourArea(c)
                  biggestIndex=index
               elif  cv2.contourArea(c)>secondSize:
                  secondSize=cv2.contourArea(c)
                  secondIndex=index
               index=index+1
               
           
        
        if biggestIndex>-1:
           cv2.drawContours(backtorgb, contours, biggestIndex, (0,255,0), 1)
           brect1=cv2.minAreaRect(contours[biggestIndex])
           brectPoints=cv2.boxPoints(brect1)
           brectPoints=np.int0(brectPoints)
           cv2.drawContours(backtorgb,[brectPoints],0,(0,0,255),1)
           boxText="("+str(brectPoints[0][0])+","+str(brectPoints[0][1])+")"+"("+str(brectPoints[1][0])+","+str(brectPoints[1][1])+")""("+str(brectPoints[2][0])+","+str(brectPoints[2][1])+")""("+str(brectPoints[3][0])+","+str(brectPoints[3][1])+")"
           #cv2.putText(backtorgb, boxText,(3, 233), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           if self.written==False:
              self.datafile.write(boxText)
              self.datafile.write("\n")
        if secondIndex>-1:
           cv2.drawContours(backtorgb, contours, secondIndex, (0,255,0), 1)
           brect2=cv2.minAreaRect(contours[secondIndex])
           brectPoints2=cv2.boxPoints(brect2)

           brectPoints2=np.int0(brectPoints2)
           boxText="("+str(brectPoints2[0][0])+","+str(brectPoints2[0][1])+")"+"("+str(brectPoints2[1][0])+","+str(brectPoints2[1][1])+")""("+str(brectPoints2[2][0])+","+str(brectPoints2[2][1])+")""("+str(brectPoints2[3][0])+","+str(brectPoints2[3][1])+")"
           cv2.putText(backtorgb, boxText,(3, 233), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           cv2.drawContours(backtorgb,[brectPoints2],0,(0,0,255),1)
           if self.written==False:
              self.datafile.write(boxText)
              self.datafile.write("\n")
            

           #if you are here, there must be two contours.  Find the appropriate
           #corners


           v1=321 #there ought to be an easier way, but......
           v2=321
           v3=321
           v4=321
           
           v1i=-1
           v2i=-1
           v3i=-1
           v4i=-1

           #This is possibly the dumbest sort I've ever done.  But it works and I was tired.
           #It is really a modification of some earlier code, that made sense.
           
           for index in range(0,4):
              if brectPoints[index][1]<v1:
                v4i=v3i
                v3i=v2i
                v2i=v1i
                v1i=index

                v4=v3
                v3=v2
                v2=v1
                v1=brectPoints[index][1]
              elif brectPoints[index][1]<v2:
                v4i=v3i
                v3i=v2i
                v2i=index

                v4=v3
                v3=v2
                v2=brectPoints[index][1]
              elif brectPoints[index][1]<v3:
                v4i=v3i
                v3i=index

                v4=v3
                v3=brectPoints[index][1]
              else:
                v4i=index
                v4=brectPoints[index][1]
                
            
           point1_1=brectPoints[v1i]
           point2_1=brectPoints[v2i]
           point3_1=brectPoints[v3i]
           point4_1=brectPoints[v4i]


           v1=321 #there ought to be an easier way, but......
           v2=321
           v3=321
           v4=321
           
           v1i=-1
           v2i=-1
           v3i=-1
           v4i=-1

           for index in range(0,4):
              if brectPoints2[index][1]<v1:
                v4i=v3i
                v3i=v2i
                v2i=v1i
                v1i=index

                v4=v3
                v3=v2
                v2=v1
                v1=brectPoints2[index][1]
              elif brectPoints2[index][1]<v2:
                v4i=v3i
                v3i=v2i
                v2i=index

                v4=v3
                v3=v2
                v2=brectPoints2[index][1]
              elif brectPoints2[index][1]<v3:
                v4i=v3i
                v3i=index

                v4=v3
                v3=brectPoints2[index][1]
              else:
                v4i=index
                v4=brectPoints2[index][1]
                
            
           point1_2=brectPoints2[v1i]
           point2_2=brectPoints2[v2i]
           point3_2=brectPoints2[v3i]
           point4_2=brectPoints2[v4i]

           
           #Almost there - set up the arrays of object and image points
        
           x1=point1_1[0]
           x2=point1_2[0]
           imagepoints=np.array((point1_1,point2_1,point3_1,point4_1,point1_2,point2_2,point3_2,point4_2),dtype=np.float)
           
    #       logstring(str(imagepoints))
           

           if (x1<x2) :
                objpoints=np.array(((-5.94,0.5,0),(-4,0,0),(-7.32,-4.82,0),(-5.38,-5.32,0),(5.94,0.5,0),(4,0,0),(7.32,-4.82,0),(5.38,-5.32,0)),dtype=np.float)
           else:
                objpoints=np.array(((5.94,0.5,0),(4,0,0),(7.32,-4.82,0),(5.38,-5.32,0),(-5.94,0.5,0),(-4,0,0),(-7.32,-4.82,0),(-5.38,-5.32,0)),dtype=np.float)

         
           

           #imagepoints=np.array(((186,220),(188,212),(187,171),(186,164)),dtype=np.float)
           cv2.putText(backtorgb, str(imagepoints[4][0])+" "+str(imagepoints[4][1]),(3, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           cv2.putText(backtorgb, str(imagepoints[5][0])+" "+str(imagepoints[5][1]),(3, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           cv2.putText(backtorgb, str(imagepoints[6][0])+" "+str(imagepoints[6][1]),(3, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           cv2.putText(backtorgb, str(imagepoints[7][0])+" "+str(imagepoints[7][1]),(3, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
      
      #     cv2.putText(backtorgb, str(topcorner1[0])+" "+str(topcorner1[1]),(160,65),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
      #     cv2.putText(backtorgb, str(secondcorner1[0])+" "+str(secondcorner1[1]),(160,85),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
      #     cv2.putText(backtorgb, str(topcorner2[0])+" "+str(topcorner2[1]),(160,105),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
      #     cv2.putText(backtorgb, str(secondcorner2[0])+" "+str(secondcorner2[1]),(160,125),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           #The moment of truth?
           errorestimate,rvec,tvec=cv2.solvePnP(objpoints,imagepoints,self.cameraMatrix,self.distcoeff)

           #cv2.putText(backtorgb, str(tvec[0])+" "+str(tvec[1])+" "+str(tvec[2]),(3, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           cv2.putText(backtorgb, "%.2f" % tvec[0]+" "+"%.2f" % tvec[1]+" "+"%.2f" % tvec[2],(3, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           
           cv2.putText(backtorgb, "%.2f" % (rvec[0]*180/3.14159)+" "+  "%.2f" % (rvec[1]*180/3.14159)+" "+"%.2f" % (rvec[2]*180/3.14159),(3, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
          
           #spit things out on the serial port, but first, do some testing.  Print stuff out.                   


       
           #change coordinate systems

           ZYX,jac=cv2.Rodrigues(rvec)

           yaw=0
           yaw=self.rotationMatrixToEulerAngles(ZYX)
#Now we have a 3x3 rotation matrix, and a translation vector. Form the 4x4 transformation matrix using homogeneous coordinates.
#There are probably numpy functions for array/matrix manipulations that would make this easier, but I don?t know them and this works.
           totaltransformmatrix=np.array([[ZYX[0,0],ZYX[0,1],ZYX[0,2],tvec[0]],[ZYX[1,0],ZYX[1,1],ZYX[1,2],tvec[1]],[ZYX[2,0],ZYX[2,1],ZYX[2,2],tvec[2]],[0,0,0,1]])
#The resulting array is the transformation matrix from world coordinates (centered on the target) to camera coordinates. (Centered on the camera) We need camera to world. That is just the inverse of that matrix.
           WtoC=np.mat(totaltransformmatrix)

          # inverserotmax=np.linalg.inv(totaltransformmatrix)
          # cv2.putText(backtorgb, "%.2f" % inverserotmax[0,3]+" "+"%.2f" % inverserotmax[1,3]+" "+"%.2f" % inverserotmax[2,3],(3, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           cv2.putText(backtorgb, "%.2f" % yaw,(3, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        
           processedFileName="output"+str(self.currentimagecount-1)+".png"
    #       cv2.imwrite(processedFileName,backtorgb)        
           cv2.imwrite("output7354.png",backtorgb)
        
 
 
 
 
       # cv2.putText(outimg, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        
        # Convert our output image to video output format and send to host over USB:
        outframe.sendCv(backtorgb)
        self.written=True
        

            
#    def writeToScreen(self, screenString, selectedImage,startX, startY):
#         cv2.putText(selectedImage,screenString,)(startX,startY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
          
    
    
        
        
