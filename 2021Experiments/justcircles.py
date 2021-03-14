import cv2
import numpy as np
import math
import time
import sys
import threading

filename="/home/pi/testpics/posout/gray_252_4.png"
grayCropped=cv2.imread(filename)
cv2.imshow('original',grayCropped)
grayCropped=cv2.cvtColor(grayCropped,cv2.COLOR_BGR2GRAY)
 
circles=None
circles = cv2.HoughCircles(grayCropped,cv2.HOUGH_GRADIENT,1,30,param1=55,param2=14,minRadius=15,maxRadius=150)
grayCropped=cv2.cvtColor(grayCropped,cv2.COLOR_GRAY2BGR)

if circles is None: 
    print("No circles")
else:
    circles = np.uint16(np.around(circles))
    howmany=0
    for circ in circles[0,:]:
        if (circ[2]==0):
                print("deleting a zero radius circle")
                continue
        print(str(circ[0])+" "+str(circ[1])+" "+str(circ[2])+" ")
        howmany+=1
        cv2.circle(grayCropped,(circ[0],circ[1]),circ[2],(255,0,0),2)
        
cv2.imshow('circles',grayCropped)    
cv2.waitKey(0)
cv2.destroyAllWindows()