import libjevois as jevois
import cv2
import numpy as np
import math
import random

## x
#
# Add some description of your module here.
#
# @author DAve
# 
# @videomapping YUYV 640 480 30 YUYV 640 480 30 X Sandbox2
# @email none
# @address 123 first street, Los Angeles CA 90012, USA
# @copyright Copyright (C) 2018 by DAve
# @mainurl none
# @supporturl none
# @otherurl none
# @license GPL v3
# @distribution Unrestricted
# @restrictions None
# @ingroup modules
class Cargo:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("processing timer", 100, jevois.LOG_INFO)
        
        # a simple frame counter used to demonstrate sendSerial():
        self.frame = 0

        self.FocalLengthPixels=335
        self.imagecount=random.randint(1,50001)
        self.datafilename="datafile"+str(self.imagecount)+".txt"
        self.datafile=open(self.datafilename,"w+")

        
    # ###################################################################################################
    ## Process function with no USB output
    def processNoUSB(self, inframe):
        # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR. If you need a
        # grayscale image, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB() and getCvRGBA():
        inimg = inframe.getCvBGR()

        
        
    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe, outframe):
         # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR. If you need a
        # grayscale image, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB() and getCvRGBA():
        inimg = inframe.getCvBGR()
        if (self.imagecount%20==0):
            self.datafile.close() #Close it periodically to save contents
            self.datafile=open(self.datafilename,"a")
        imagefilename="saveimage"+str(self.imagecount)+".png"
        cv2.imwrite(imagefilename, inimg)  

        
        #If we know anything about the location of the object, ignore the area we don?t care about
        #crop the image to the only place where balls might be.

       # yshift=54  #save the number of pixels to offset by in the final calculation
       # croppedImage=inimg[294:480,0:639,0:3]


        #croppedImage=inimg[294:480,0:639,0:3]
        

        
        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()
    


        blurred=cv2.medianBlur(inimg,7)

        #Perform feature recognition tasks to identify possible objects.

        #The objects we are looking for are orange, so pick out orange things.
        #These numbers came from running GRIP
        #lowColor=np.array([40,140,60])
        #highColor=np.array([80,174,140])
        lowColor=np.array([0,10,200])
        highColor=np.array([14,100,255])
        imghls = cv2.cvtColor(blurred, cv2.COLOR_BGR2HLS)
        
        mask=cv2.inRange(imghls,lowColor,highColor)


        #Taking out everything that isn't orange might have removed some good stuff, too
        #The dilation will do a little bit to fill back in some of the missing pixels, but it
        #will distort the shape a bit in the areas where it got it right.  Tradeoffs.

        edges=cv2.Canny(mask,20,200)
        circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,1,20,param1=100,param2=20,minRadius=0,maxRadius=0)
        if circles is not None:
           mask=cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
           circles=np.around(circles)

           circles = np.uint16(circles)
           
           stupid=False
           for i in circles[0,:]:
        # draw the outer circle
              cv2.circle(mask,(i[0],i[1]),i[2],(0,255,0),2)
  #      # draw the center of the circle
              cv2.circle(mask,(i[0],i[1]),2,(0,0,255),3)
              if (stupid==False):
                 xCenter=i[0]-160  #320x240 resolution, y axis down.
                 yCenter=i[1]-120
                 rBall=i[2]  #Radius of ball, in pixels
                 stupid=True




           #Now do the similar triangles thing.  I wish I could draw a diagram here.

           leftEdge=xCenter-rBall
           rightEdge=xCenter+rBall

           if (leftEdge>0) or (rightEdge<0):
              DPixels=math.sqrt(xCenter*xCenter+self.FocalLengthPixels*self.FocalLengthPixels)
              dInches=(13/2)*DPixels/rBall
              
           else:
              DPixels=-1  #not meaningful
              dInches=13*self.FocalLengthPixels/(rightEdge-leftEdge)

           theta=np.arctan(xCenter/self.FocalLengthPixels)
           xCoord=dInches*np.sin(theta)
           yCoord=dInches*np.cos(theta)
              
           self.datafile.write(str(self.imagecount)+" found a ball\n");
           self.datafile.write(str(xCenter))
           self.datafile.write(" ")
           self.datafile.write(str(yCenter))
           self.datafile.write(" ")
           self.datafile.write(str(rBall))
           self.datafile.write(" ")
           self.datafile.write(str(DPixels))
           self.datafile.write(" ")
           self.datafile.write(str(dInches))
           self.datafile.write(" ")
           self.datafile.write(str(theta))
           self.datafile.write(" ")
           self.datafile.write(str(xCoord))
           self.datafile.write(" ")
           self.datafile.write(str(yCoord))
           jevois.sendSerial("Ball "+str(xCoord)+" "+str(yCoord)+" "+str(theta))
                               
        else:
           self.datafile.write(str(self.imagecount)+" no ball\n");
         
         #hard code data from config files, for now
        self.imagecount+=1
        outimg = mask
        outframe.sendCv(outimg)
        
    # ###################################################################################################
    ## Parse a serial command forwarded to us by the JeVois Engine, return a string
    def parseSerial(self, str):
        jevois.LINFO("parseserial received command [{}]".format(str))
        if str == "hello":
            return self.hello()
        return "ERR Unsupported command"
    
    # ###################################################################################################
    ## Return a string that describes the custom commands we support, for the JeVois help message
    def supportedCommands(self):
        # use \n seperator if your module supports several commands
        return "hello - print hello using python"

    # ###################################################################################################
    ## Internal method that gets invoked as a custom command
    def hello(self):
        return "Hello from python!"
        
