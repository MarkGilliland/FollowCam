import pyvirtualcam # https://github.com/letmaik/pyvirtualcam
import numpy as np #pip install numpy
import cv2 #pip install opencv-python
import time
from statistics import mean

cap = 0;
i = 0;
while True:
    cap = cv2.VideoCapture(i)
    if cap.isOpened() == False:
        input("No valid webcams found. Press enter to retry search, ctrl+c to quit")
        i = 0
        continue
    if cap.getBackendName() != 'DSHOW':
        break
    else:
        cap.release()
        i = i + 1

print(cap.getBackendName())
capWidth = 1280
capHeight = 720
cap.set(3, capWidth)
cap.set(4, capHeight)
cap.read()

primary_cascade   = cv2.CascadeClassifier('haarCascades/haarcascade_frontalface_alt_tree.xml')
secondary_cascade = cv2.CascadeClassifier('haarCascades/haarcascade_frontalface_alt2.xml')
tertiary_cascade  = cv2.CascadeClassifier('haarCascades/haarcascade_profileface.xml')
eyes_cascade      = cv2.CascadeClassifier('haarCascades/haarcascade_eye_tree_eyeglasses.xml')

font = cv2.FONT_HERSHEY_SIMPLEX

minFaceSize = 100 #Minimum size of face to detect. At 720p,  is roughly 12ft away


cvScaleFactor = 4
cvWidth = int(capWidth/cvScaleFactor)
cvHeight = int(capHeight/cvScaleFactor)
smallestFeature = tuple([int(minFaceSize//cvScaleFactor)])*2


fpsList = [0.03]

with pyvirtualcam.Camera(width=capWidth, height=capHeight, fps=20, delay=0) as cam:
    progStart = time.time()
    #while(time.time() - progStart < 30):
    while(True):
        startOfFrame = time.time()
        
        ret, capFrame = cap.read()

        
        editedFrame = capFrame

        

        # Read the input image
        img = cv2.resize(capFrame, (cvWidth, cvHeight))
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect faces
        rectColor = (0, 0, 0)
        faces = primary_cascade.detectMultiScale(gray, 1.1, minSize = smallestFeature)
        rectColor = (100, 0, 0)
        if len(faces) == 0:
            faces = secondary_cascade.detectMultiScale(gray, 1.1, minSize = smallestFeature)
            rectColor = (0, 100, 0)
        if len(faces) == 0:
            faces = tertiary_cascade.detectMultiScale(gray, 1.1, minSize = smallestFeature)
            rectColor = (0, 0, 100)
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(editedFrame, (cvScaleFactor*x, cvScaleFactor*y), (cvScaleFactor*(x+w), cvScaleFactor*(y+h)), rectColor, 4)
        
        #format the frame for the camera output, adding a 4th channel
        editedFrame4ch = np.ones((cam.height, cam.width, 4), np.uint8)*255 # RGBA
        editedFrame4ch[:, :, 0:3] = cv2.cvtColor(editedFrame, cv2.COLOR_BGR2RGB)
        
        cam.send(editedFrame4ch)

        fpsList.append(time.time() - startOfFrame)
        cam.sleep_until_next_frame()


cap.release()
fpsList[0] = fpsList[2]
fpsList[1] = fpsList[2]
print("Min  FPS: {}".format(1/max(fpsList)))
print("Mean FPS: {}".format(1/mean(fpsList)))
print("Max  FPS: {}".format(1/min(fpsList)))
