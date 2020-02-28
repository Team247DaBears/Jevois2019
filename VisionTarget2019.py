import libjevois as jevois
import cv2
import numpy as np

## Detect pairs of targets
#
# Add some description of your module here.
#
# @author Dave
# 
# @videomapping YUYV 640 480 30 YUYV 640 480 30 Dave VisionTarget2019
# @email 
# @address 123 first street, Los Angeles CA 90012, USA
# @copyright Copyright (C) 2018 by Dave
# @mainurl 
# @supporturl 
# @otherurl 
# @license 
# @distribution Unrestricted
# @restrictions None
# @ingroup modules
class VisionTarget2019:
    # ###################################################################################################
    ## Constructor

    # ###################################################################################################
    ## Constructor
    def __init__(self):
        # Instantiate a JeVois Timer to measure our processing framerate:

        self.cameraMatrix=np.zeros((3,3))
        self.cameraMatrix[0][0]=335.0
        self.cameraMatrix[0][2]=170
        self.cameraMatrix[1][1]=335
        self.cameraMatrix[1][2]=121
        self.cameraMatrix[2][2]=1
        
        self.distcoeff=np.zeros((1,5))
        self.distcoeff[0][0]=0.20
        self.distcoeff[0][1]=-0.81
        self.distcoeff[0][2]=-0.008
        self.distcoeff[0][3]=-0.003
        self.distcoeff[0][4]=-8
        
        self.distcoeff[0][0]=0
        self.distcoeff[0][1]=0
        self.distcoeff[0][2]=0
        self.distcoeff[0][3]=0
        self.distcoeff[0][4]=0
        
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
        
        imagefilename="saveimage6200.png"
        
        inimg = cv2.imread(imagefilename)
        
        objpoints=np.array(((-5.94,0.5,0),(-4,0,0),(4,0,0),(5.94,0.5,0)),dtype=np.float)
        imagepoints=np.array(((9,72),(14,75),(38,71),(44,65)),dtype=np.float)
              
        #The moment of truth?
        errorestimate,rvec,tvec=cv2.solvePnP(objpoints,imagepoints,self.cameraMatrix,self.distcoeff)

           #cv2.putText(backtorgb, str(tvec[0])+" "+str(tvec[1])+" "+str(tvec[2]),(3, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        cv2.putText(inimg, "%.2f" % tvec[0]+" "+"%.2f" % tvec[1]+" "+"%.2f" % tvec[2],(3, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
           
        cv2.putText(inimg, "%.2f" % (rvec[0]*180/3.14159)+" "+  "%.2f" % (rvec[1]*180/3.14159)+" "+"%.2f" % (rvec[2]*180/3.14159),(3, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
          
           #spit things out on the serial port, but first, do some testing.  Print stuff out.                   
                    

        ZYX,jac=cv2.Rodrigues(rvec)
       # totalrotmax=np.array([[ZYX[0,0],ZYX[0,1],ZYX[0,2],tvec[0]],[ZYX[1,0],ZYX[1,1],ZYX[1,2],tvec[1]],[ZYX[2,0],ZYX[2,1],ZYX[2,2],tvec[2]],[0,0,0,1]])
       # totalrotmax=np.array([[1,0,0,0].[0,1,0,0],[0,0,1,0],[0,0,0,1]])
       # totalrotmax = np.array([[1, 0, 0, 0],
       #         [0, 1, 0, 0],
       #         [0, 0, 1,0],
       #         [0, 0, 0, 1]])
       # WtoC=np.mat(totalrotmax)
       # inverserotmax=np.linalg.inv(WtoC)
       # f=inverserotmax 
       # a=1.234
       #cv2.putText(inimg, "%.2f" % (f[0,3]}+" "+  "%.2f" % (f[1,3)+" "+"%.2f" % (f[2,3]),(3, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
       #cv2.putText(inimg, "%.2f" % a+" "+  "%.2f" % a+" "+"%.2f" % a,(3, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        
             
                   

        
 
 
 
 
       # cv2.putText(outimg, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        
        # Convert our output image to video output format and send to host over USB:
        outframe.sendCv(inimg)
        self.written=True
        

        
