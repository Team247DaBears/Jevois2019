import libjevois as jevois
import cv2
import numpy as np

## Serial
#
# Add some description of your module here.
#
# @author 
# 
# @videomapping YUYV 320 240 30 YUYV 320 240 30 Dave JustSerial
# @email 
# @address 123 first street, Los Angeles CA 90012, USA
# @copyright Copyright (C) 2018 by 
# @mainurl 
# @supporturl 
# @otherurl 
# @license 
# @distribution Unrestricted
# @restrictions None
# @ingroup modules
class JustSerial:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        # Instantiate a JeVois Timer to measure our processing framerate:
        self.timer = jevois.Timer("processing timer", 100, jevois.LOG_INFO)
        
    # ###################################################################################################
    ## Process function with USB output
        ## Process function with no USB output
    def processNoUSB(self, inframe):
        img = inframe.getCvBGR()
        jevois.sendSerial("A 2.34 ")

    def process(self, inframe, outframe):
        # Get the next camera image (may block until it is captured) and here convert it to OpenCV BGR. If you need a
        # grayscale image, just use getCvGRAY() instead of getCvBGR(). Also supported are getCvRGB() and getCvRGBA():
        inimg = inframe.getCvBGR()
        jevois.sendSerial("A 1.23")
        outframe.sendCv(inimg)
        
