





import libjevois as jevois
import cv2
import numpy as np
import random

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
        self.cameraMatrix[0][2]=160
        self.cameraMatrix[1][1]=329
        self.cameraMatrix[1][2]=120
        self.cameraMatrix[2][2]=1
        
        self.distcoeff=np.zeros((1,5))
        self.distcoeff[0][0]=0.236
        self.distcoeff[0][1]=-0.290
        self.distcoeff[0][2]=-0.00115
        self.distcoeff[0][3]=-0.00087
        self.distcoeff[0][4]=-2.4
        
        self.distcoeff[0][0]=0
        self.distcoeff[0][1]=0
        self.distcoeff[0][2]=0
        self.distcoeff[0][3]=0
        self.distcoeff[0][4]=0
        
        self.currentimagecount=random.randint(1,50001)
        self.datafile=open("targetData.txt","w+")
        self.written=False

        
        
        

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
        # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR. If you need a
        # grayscale image, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB() and getCvRGBA():
       # self.currentloopcount=self.currentloopcount+1
       # if self.currentloopcount==self.maxloopcount:
       #    self.currentimagecount=self.currentimagecount+1
       #    self.currentloopcount=0
       #    if self.currentimagecount>self.maximagecount:
       #       self.currentimagecount=self.minimagecount
       # self.currentimagecount=242
        
        imagefilename="practice"+str(self.currentimagecount)+".png"
        
#        inimg = cv2.imread(imagefilename+)
        inimg=cv2.imread("practice45719.png")      
        
#
#        inimg=inframe.getCvBGR()
        self.currentimagecount+=1
#        cv2.imwrite(imagefilename,inimg)
        inimg=cv2.transpose(inimg)
        inimg=cv2.flip(inimg, 1)
        

        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()

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
          #        cv2.putText(backtorgb, str(cv2.contourArea(c)),(3, 233), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
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

           topmost=321 #there ought to be an easier way, but......
           secondmost=321
           toppointindex=-1
           secondpointindex=-1
           
           for index in range(0,4):
              if brectPoints[index][1]<topmost:
                secondpointindex=toppointindex
                toppointindex=index
                secondmost=topmost
                topmost=brectPoints[index][1]
                if self.written==False:
                    self.datafile.write("Topmost index is now "+str(index)+"\n")
              elif brectPoints[index][1]<secondmost:
                secondpointindex=index
                secondmost=brectPoints[index][1]
                if self.written==False:
                    self.datafile.write("Secondmost index is now "+str(index)+"\n")
                
           topcorner1=brectPoints[toppointindex]
           secondcorner1=brectPoints[secondpointindex]

           topmost=321 #there ought to be an easier way, but......
           secondmost=321
           toppointindex=-1
           secondpointindex=-1
           if self.written==False:
              self.datafile.write("Next set of points \n")
           for index in range(0,4):
              if self.written==False:
                 self.datafile.write(str(topmost)+" "+str(secondmost)+" "+str(brectPoints2[index][1])+"\n")
              if brectPoints2[index][1]<topmost:
                secondpointindex=toppointindex
                toppointindex=index
                secondmost=topmost
                topmost=brectPoints2[index][1]
                if self.written==False:
                    self.datafile.write("Topmost index is now "+str(index)+"\n")

              elif brectPoints2[index][1]<secondmost:
                secondpointindex=index
                secondmost=brectPoints2[index][1]
                if self.written==False:
                    self.datafile.write("Secondmost index is now "+str(index)+"\n")
                
           topcorner2=brectPoints2[toppointindex]
           secondcorner2=brectPoints2[secondpointindex]
           #Almost there - set up the arrays of object and image points
           #cv2.putText(backtorgb, str(topcorner2[0])+" "+str(topcorner2[1]),(3, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
      
           objpoints=np.array(((-5.94,0.5,0),(-4,0,0),(4,0,0),(5.94,0.5,0)),dtype=np.float)
           x1=topcorner1[0]
           x2=topcorner2[0]
           if x1<x2:
               imagepoints=np.array([[topcorner1[0],topcorner1[1]],[secondcorner1[0],secondcorner1[1]],[secondcorner2[0],secondcorner2[1]],[topcorner2[0],topcorner2[1]]],dtype=np.float)
               
           else:
               imagepoints=np.array([[topcorner2[0],topcorner2[1]],[secondcorner2[0],secondcorner2[1]],[secondcorner1[0],secondcorner1[1]],[topcorner1[0],topcorner1[1]]],dtype=np.float)
         #  imagepoints=np.array(((50*(-5.94)+320,50*0.5+240),(50*(-4)+320,0+240),(50*4+320,0+240),(50*5.94+320,50*0.5+240)),dtype=np.float)
              

           #imagepoints=np.array(((186,220),(188,212),(187,171),(186,164)),dtype=np.float)
           cv2.putText(backtorgb, str(imagepoints[0][0])+" "+str(imagepoints[0][1]),(3, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           cv2.putText(backtorgb, str(imagepoints[1][0])+" "+str(imagepoints[1][1]),(3, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           cv2.putText(backtorgb, str(imagepoints[2][0])+" "+str(imagepoints[2][1]),(3, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           cv2.putText(backtorgb, str(imagepoints[3][0])+" "+str(imagepoints[3][1]),(3, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
      
           cv2.putText(backtorgb, str(topcorner1[0])+" "+str(topcorner1[1]),(160,65),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           cv2.putText(backtorgb, str(secondcorner1[0])+" "+str(secondcorner1[1]),(160,85),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           cv2.putText(backtorgb, str(topcorner2[0])+" "+str(topcorner2[1]),(160,105),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           cv2.putText(backtorgb, str(secondcorner2[0])+" "+str(secondcorner2[1]),(160,125),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           #The moment of truth?
           errorestimate,rvec,tvec=cv2.solvePnP(objpoints,imagepoints,self.cameraMatrix,self.distcoeff)

           #cv2.putText(backtorgb, str(tvec[0])+" "+str(tvec[1])+" "+str(tvec[2]),(3, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           cv2.putText(backtorgb, "%.2f" % tvec[0]+" "+"%.2f" % tvec[1]+" "+"%.2f" % tvec[2],(3, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           
           cv2.putText(backtorgb, "%.2f" % (rvec[0]*180/3.14159)+" "+  "%.2f" % (rvec[1]*180/3.14159)+" "+"%.2f" % (rvec[2]*180/3.14159),(3, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
          
           #spit things out on the serial port, but first, do some testing.  Print stuff out.                   
                    

              
                   

        
 
 
 
 
       # cv2.putText(outimg, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        
        # Convert our output image to video output format and send to host over USB:
        outframe.sendCv(backtorgb)
        self.written=True
        
