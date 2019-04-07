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
class Sandbox2:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("processing timer", 100, jevois.LOG_INFO)
        
        # a simple frame counter used to demonstrate sendSerial():
        self.frame = 0
        
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

        yshift=54  #save the number of pixels to offset by in the final calculation
        croppedImage=inimg[294:480,0:639,0:3]

                yshift=54  #save the number of pixels to offset by in the final calculation
        croppedImage=inimg[294:480,0:639,0:3]
        
        jevois.sendSerial("in x "+str(len(inimg)))
        jevois.sendSerial("in y "+str(len(inimg[0])))
        jevois.sendSerial("in color "+str(len(inimg[0][0])))
        
        jevois.sendSerial("out x "+str(len(croppedImage)))
        jevois.sendSerial("out y "+str(len(croppedImage[0])))
        jevois.sendSerial("out color "+str(len(croppedImage[0][0])))
        
        # Start measuring image processing time (NOTE: does not account for input conversion time):
        self.timer.start()
    
        # Detect edges using the Laplacian algorithm from OpenCV:
        #
        # Replace the line below by your own code! See for example
        # - http://docs.opencv.org/trunk/d4/d13/tutorial_py_filtering.html
        # - http://docs.opencv.org/trunk/d9/d61/tutorial_py_morphological_ops.html
        # - http://docs.opencv.org/trunk/d5/d0f/tutorial_py_gradients.html
        # - http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html
        #
        # and so on. When they do "img = cv2.imread('name.jpg', 0)" in these tutorials, the last 0 means they want a
        # gray image, so you should use getCvGRAY() above in these cases. When they do not specify a final 0 in imread()
        # then usually they assume color and you should use getCvBGR() above.
        #
        # The simplest you could try is:
        #    outimg = inimg
        # which will make a simple copy of the input image to output.

        blurred=cv2.GaussianBlur(croppedImage,(3,3),0)

        #Perform feature recognition tasks to identify possible objects.

        #The objects we are looking for are orange, so pick out orange things.
        #These numbers came from running GRIP
        #lowColor=np.array([40,140,60])
        #highColor=np.array([80,174,140])
        lowColor=np.array([40,140,60])
        highColor=np.array([200,174,140])
        imghsv = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2HSV)


        mask=cv2.inRange(blurred,lowColor,highColor)

        #Taking out everything that isn't orange might have removed some good stuff, too
        #The dilation will do a little bit to fill back in some of the missing pixels, but it
        #will distort the shape a bit in the areas where it got it right.  Tradeoffs.


        kernel=np.ones((3,3),np.uint8) #Maybe necessary for smoothing a bit
        dilmask= cv2.dilate(mask,kernel,iterations=1)


        #Balls will mostly big blobs of uniform color.  Contours are actually easier to
        #work with than blobs, so we'll find contours
        contours, hierarchy = cv2.findContours(dilmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        
        #Perform tests on those features to select the best match for the object we are looking for
        
        #There aren't many big orange things out there, so the biggest one is probably
        #the closest ball.  Find the biggest one.
        biggest=0
        biggestContour=None
        for cnt in contours:
            cnt_area = cv2.contourArea(cnt, True)
            if cnt_area>biggest:
                biggest=cnt_area
                biggestContour=cnt

        #Compute the real world location of the object based on what we know from its image.        
        if biggest<20:
            BallFound=False
        else:
           #The center of the object (ball) can be approximated by the center of the bounding rectangle,
           #The bounding rectangle is the smallest rectangle that completely encloses the object.                   
           x,y,w,h=cv2.boundingRect(cnt)

           #The first thing we are interested in is the angle from the ball to our robot.
           #Find the center of that square, in image coordinates (0,0) is the center of the
           #picture.  The coordinates of the image matrix have 0,0 in the top left corner                   
           centerX=(x+w/2)-320
                              
          
           angleOfBall=np.arctan(centerX/658.0) #658.0 is the focal length in pixels
           angleDegrees=angleOfBall*180.0/3.1416

           #We may also care about distance
           #Find the Y center of the axis
           centerY=y+54   #Remember we through out the entire top half, plus 54 pixels.
           #D=hF/Y
           distance=24*658/centerY  #24 is h, the number of inches from the camera to the ball                   
           BallFound=True
                              
         #Tell the robot what we learned.                     
        if BallFound:
           jevois.sendSerial("Ball "+str(angleOfBall)+" "+str(distance))
        else:
           jevois.sendSerial("No ball found this cycle")
                              

        
        
         
         #hard code data from config files, for now
         
        outimg = mask
        # Write frames/s info from our timer into the edge map (NOTE: does not account for output conversion time):
        fps = self.timer.stop()
        height = outimg.shape[0]
        width = outimg.shape[1]
        outframe.sendCv(outimg)
  #     # cv2.putText(outimg, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        # cv2.putText(outimg, str(len(squares)), (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
        
      

      
        self.frame += 1
        
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
        
