#Capture fifty images from usb webam zero Raspberry Pi
import cv2

cap = cv2.VideoCapture(0)
if cap.isOpened():
   print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
   print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
   print(cap.get(cv2.CAP_PROP_FPS))
   print(cap.get(cv2.CAP_PROP_BRIGHTNESS))
   print(cap.get(cv2.CAP_PROP_CONTRAST))
   print(cap.get(cv2.CAP_PROP_SATURATION))
   print(cap.get(cv2.CAP_PROP_HUE))
   print(cap.get(cv2.CAP_PROP_GAIN))
   print(cap.get(cv2.CAP_PROP_EXPOSURE))
   
   cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
   cap.set(cv2.CAP_PROP_BRIGHTNESS,0)
   
    
   ret, frame = cap.read()
   cv2.imwrite("brightness0.png",frame)
   #savefilename="saveimage"+str(i)+".png"
   #cv2.imwrite(savefilename,frame)
   #ret=True;
else:
   ret=False
print(ret)
cv2.imshow('frame',frame)
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()