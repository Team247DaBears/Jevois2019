import libjevois as jevois
import cv2
import numpy as np

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
class RocketSolvePnP:
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
        self.maxloopcount=10

        self.cameraMatrix=np.zeros((3,3))
        self.cameraMatrix[0][0]=659.0
        self.cameraMatrix[0][2]=342
        self.cameraMatrix[1][1]=658
        self.cameraMatrix[1][2]=250
        self.cameraMatrix[2][2]=1
        
        self.distcoeff=np.zeros((1,5))
        self.distcoeff[0][0]=0.236
        self.distcoeff[0][1]=-0.290
        self.distcoeff[0][2]=-0.00115
        self.distcoeff[0][3]=-0.00087
        self.distcoeff[0][4]=-2.4

        
        
        

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

        imagefilename="saveimage12224.png"
        inimg = cv2.imread(imagefilename)
        backtorgb=inimg
      
        objpoints=np.array(((-24,0,-24.8),(-10.25,0,0),(10.25,0,0),(24,0,-24.8)),dtype=np.float)
        imagepoints=np.array([[116,324],[177,387],[401,398],[474,348]],dtype=np.float)
        
         
           #The moment of truth?
        errorestimate,rvec,tvec=cv2.solvePnP(objpoints,imagepoints,self.cameraMatrix,self.distcoeff)

        cv2.putText(backtorgb, str(tvec[0])+" "+str(tvec[1])+" "+str(tvec[2]),(3, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        cv2.putText(backtorgb, str(rvec[0])+" "+str(rvec[1])+" "+str(rvec[2]),(3, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
          
           #spit things out on the serial port, but first, do some testing.  Print stuff out.                   
                    

              
                   

        
 
 
 
 
       # cv2.putText(outimg, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        
        # Convert our output image to video output format and send to host over USB:
        outframe.sendCv(backtorgb)
        
