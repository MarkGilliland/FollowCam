import pyvirtualcam # https://github.com/letmaik/pyvirtualcam
import numpy as np #pip install numpy
import cv2 #pip install opencv-python
import time
from statistics import mean

cap = cv2.VideoCapture(0)
capWidth = 1280
capHeight = 720
cap.set(3, capWidth)
cap.set(4, capHeight)

face_cascade = cv2.CascadeClassifier('haarCascades/haarcascade_frontalface_alt_tree.xml')

cvScaleFactor = 5
cvWidth = int(capWidth/cvScaleFactor)
cvHeight = int(capHeight/cvScaleFactor)

fpsList = []

with pyvirtualcam.Camera(width=capWidth, height=capHeight, fps=30) as cam:
    progStart = time.time()
    #while(time.time() - progStart < 4):
    while(True):
        startOfFrame = time.time()
        
        ret, capFrame = cap.read()

        
        editedFrame = capFrame

        # Read the input image
        img = cv2.resize(capFrame, (cvWidth, cvHeight))
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(editedFrame, (cvScaleFactor*x, cvScaleFactor*y), (cvScaleFactor*(x+w), cvScaleFactor*(y+h)), (255, 0, 0), 2)
        # Display the output

        
        
        #format the frame for the camera output, adding a 4th channel
        editedFrame4ch = np.ones((cam.height, cam.width, 4), np.uint8)*255 # RGBA
        editedFrame4ch[:, :, 0:3] = cv2.cvtColor(editedFrame, cv2.COLOR_BGR2RGB)
        
        cam.send(editedFrame4ch)

        fpsList.append(time.time() - startOfFrame)
        #cam.sleep_until_next_frame()

cap.release()
fpsList[0] = fpsList[1]
print("Min  FPS: {}".format(1/min(fpsList)))
print("Mean FPS: {}".format(1/mean(fpsList)))
print("Max  FPS: {}".format(1/max(fpsList)))
