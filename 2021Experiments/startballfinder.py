import cv2
import numpy as np
import math
import time
import sys


imageCounter=10
maxSeconds=120
delaySeconds=10

imageHeight=480
imageWidth=640
cameraFOV=45

   


#yellow
lowColor=np.array([19,85,130])
highColor=np.array([42,220,255])


firstTime=True    


savefilename="/home/pi/Jevois2019/2021Experiments/saveimage49.png"
inimg=cv2.imread(savefilename)
imghls = cv2.cvtColor(inimg, cv2.COLOR_BGR2HLS)
cv2.imshow('imghls',imghls)
mask=cv2.inRange(imghls,lowColor,highColor)
cv2.imshow('mask',mask)

maxones=0
centercolumn=-1
for i in range(0,639):
    print(str(i))
    slice=mask[0:479,i]
    ones=cv2.countNonZero(slice)
    print(str(ones))
    if (ones>maxones):
        maxones=ones
        centercolumn=i
print("center column: "+str(centercolumn)+" Number of pixels: "+str(maxones))

cv2.destroyAllWindows()
sys.exit()
      
