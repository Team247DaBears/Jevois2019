import cv2
import numpy as np
import math

imagefilename="/home/pi/testpics/gray_435_0.png"

#yellow
lowColor=np.array([15,175,100])
highColor=np.array([40,255,255])

inimg = cv2.imread(imagefilename)

gray=cv2.cvtColor(inimg,cv2.COLOR_BGR2GRAY)
circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1.4,40,param1=125,param2=20,minRadius=40,maxRadius=0)
print("Hi")
if circles is not None:
    print("here")
    circles=np.around(circles)

    circles = np.uint16(circles)
           
    
    for i in circles[0,:]:
        # draw the outer circle
        print("processing")
        cv2.circle(inimg,(i[0],i[1]),i[2],(0,255,0),2)
  #      # draw the center of the circle
        cv2.circle(inimg,(i[0],i[1]),2,(0,0,255),3)

else:
    print("no circles found")
cv2.imshow('original',inimg)    
cv2.waitKey(0)
cv2.destroyAllWindows()



