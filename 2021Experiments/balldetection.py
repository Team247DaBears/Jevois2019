import cv2
import numpy as np
import math

imagefilename="saveimage1.png"

#yellow
lowColor=np.array([15,175,100])
highColor=np.array([40,255,255])

inimg = cv2.imread(imagefilename)

blurred=cv2.medianBlur(inimg,7)
imghls = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
mask=cv2.inRange(imghls,lowColor,highColor)


edges=cv2.Canny(mask,20,200)
circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,1,30,param1=100,param2=25,minRadius=0,maxRadius=0)
print("Hi")
if circles is not None:
    print("here")
    mask=cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
    circles=np.around(circles)

    circles = np.uint16(circles)
           
    
    for i in circles[0,:]:
        # draw the outer circle
        print("processing")
        cv2.circle(inimg,(i[0],i[1]),i[2],(0,255,0),2)
  #      # draw the center of the circle
        cv2.circle(inimg,(i[0],i[1]),2,(0,0,255),3)
    cv2.imshow('mask',mask)

else:
    print("no circles found")
cv2.imshow('original',inimg)    
cv2.waitKey(0)
cv2.destroyAllWindows()


