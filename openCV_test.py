import numpy as np
import cv2
 

image = cv2.imread(r'C:\Users\berka\OneDrive - University of Tennessee at Chattanooga\Research\python\kNN_Simulation_Data\IRES_Images\ires_0.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow('Original image',image)
cv2.imshow('Gray image', gray)

cv2.waitKey(0)
cv2.destroyAllWindows()
""" 
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
     
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows() """