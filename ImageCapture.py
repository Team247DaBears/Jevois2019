import libjevois as jevois
import cv2
import numpy as np
import random

## Captures images - headless
#
# Add some description of your module here.
#
# @author Dave
# 
# @videomapping YUYV 640 480 29 YUYV 640 480 29 Dave ImageCapture
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
class ImageCapture:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("processing timer", 100, jevois.LOG_INFO)
        self.imagecount=random.randint(1,50001)
        
    # ###################################################################################################
    ## Process function with no USB output
    def processNoUSB(self, inframe):
        # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR. If you need a
        # grayscale image, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB() and getCvRGBA():
        inimg = inframe.getCvBGR()
        
        imagefilename="saveimage"+str(self.imagecount)+".png"
        self.imagecount=self.imagecount+1
        
        cv2.imwrite(imagefilename, inimg)    
    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe, outframe):
        inimg = inframe.getCvBGR()
        
        imagefilename="saveimage"+str(self.imagecount)+".png"
        self.imagecount=self.imagecount+1
        
        cv2.imwrite(imagefilename, inimg) 
        
        outimg=inimg
        # Convert our output image to video output format and send to host over USB:
        outframe.sendCv(outimg)
        
