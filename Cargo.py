import libjevois as jevois
import cv2
import numpy as np

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

        self.FocalLengthPixels=658
        
    # ###################################################################################################
    ## Process function with no USB output
    def processNoUSB(self, inframe):
        # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR. If you need a
        # grayscale image, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB() and getCvRGBA():
        inimg = inframe.getCvBGR()

        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()
        
        #jevois.LINFO("Processing video frame {} now...".format(self.frame))

        # TODO: you should implement some processing.
        # Once you have some results, send serial output messages:


        centerX=400
        angleOfBall=np.arctan(centerX/658.0)
        angleDegrees=angleOfBall*180.0/3.14
        #jevois.sendSerial("Ball"+str(angleDegrees))
        jevois.sendSerial("Ball"+str(angleDegrees))

        # Get frames/s info from our timer:
        fps = self.timer.stop()

        # Send a serial output message:
        self.frame += 1
        
    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe, outframe):
         # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR. If you need a
        # grayscale image, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB() and getCvRGBA():
        inimg = inframe.getCvBGR()

        #If we know anything about the location of the object, ignore the area we don?t care about
        #crop the image to the only place where balls might be.

       # yshift=54  #save the number of pixels to offset by in the final calculation
       # croppedImage=inimg[294:480,0:639,0:3]


        #croppedImage=inimg[294:480,0:639,0:3]
        
        #jevois.sendSerial("in x "+str(len(inimg)))
        #jevois.sendSerial("in y "+str(len(inimg[0])))
        #jevois.sendSerial("in color "+str(len(inimg[0][0])))
        
        #jevois.sendSerial("out x "+str(len(croppedImage)))
        #jevois.sendSerial("out y "+str(len(croppedImage[0])))
        #jevois.sendSerial("out color "+str(len(croppedImage[0][0])))
        
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
           

           for i in circles[0,:]:
        # draw the outer circle
              cv2.circle(mask,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
              cv2.circle(mask,(i[0],i[1]),2,(0,0,255),3)


           xCenter=circles[0,0]
           yCenter=circles[0,1]
           rBall=circles[0,2]  #Radius of ball, in pixels

           #Now do the similar triangles thing.  I wish I could draw a diagram here.

           leftEdge=xCenter-rBall
           rightEdge=xCenter+rBall

           DPixels=sqrt(xCenter*xCenter+self.FocalLengthPixels*self.FocalLengthPixels)
           dInches=(13/2)*DPixels/rBall
           theta=arctan(xCenter/self.FocalLengthPixels)
           xCoord=dInches*sin(theta)
           yCoord=dInches*cos(theta)

           jevois.SerialWrite("Ball "+str(xCoord)+" "+str(yCoord)+" "+str(theta)
                              
          
        #angleOfBall=np.arctan(centerX/658.0) #658.0 is the focal length in pixels
         #  angleDegrees=angleOfBall*180.0/3.1416

           #We may also care about distance
           #Find the Y center of the axis
          # centerY=y+54   #Remember we through out the entire top half, plus 54 pixels.
           #D=hF/Y
          # distance=24*658/centerY  #24 is h, the number of inches from the camera to the ball                   
          # BallFound=True
                              
         #Tell the robot what we learned.                     
        #if BallFound:
         #  jevois.sendSerial("Ball "+str(angleOfBall)+" "+str(distance))
        #else:
         #  jevois.sendSerial("No ball found this cycle")
                              

        
        
         
         #hard code data from config files, for now
         
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
        
