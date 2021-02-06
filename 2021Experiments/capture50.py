#Capture fifty images from usb webam zero Raspberry Pi
import cv2

cap = cv2.VideoCapture(0)
if cap.isOpened():
   for i in range(1,50): 
      ret, frame = cap.read()
      savefilename="saveimage"+str(i)+".png"
      cv2.imwrite(savefilename,frame)
   ret=True;
else:
   ret=False
print(ret)
