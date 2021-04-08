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
cap.read()

primary_cascade   = cv2.CascadeClassifier('haarCascades/haarcascade_frontalface_alt_tree.xml')
secondary_cascade = cv2.CascadeClassifier('haarCascades/haarcascade_frontalface_alt2.xml')
tertiary_cascade  = cv2.CascadeClassifier('haarCascades/haarcascade_profileface.xml')
eyes_cascade      = cv2.CascadeClassifier('haarCascades/haarcascade_eye_tree_eyeglasses.xml')

minFaceSize = 100 #Minimum size of face to detect. At 720p,  is roughly 12ft away


cvScaleFactor = 2
cvWidth = int(capWidth/cvScaleFactor)
cvHeight = int(capHeight/cvScaleFactor)
smallestFeature = tuple([int(minFaceSize//cvScaleFactor)])*2


fpsList = []

with pyvirtualcam.Camera(width=capWidth, height=capHeight, fps=30) as cam:
    progStart = time.time()
    while(time.time() - progStart < 30):
    #while(True):
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
        rectColor = (255, 0, 0)
        if len(faces) == 0:
            faces = secondary_cascade.detectMultiScale(gray, 1.1, minSize = smallestFeature)
            rectColor = (0, 255, 0)
        if len(faces) == 0:
            faces = tertiary_cascade.detectMultiScale(gray, 1.1, minSize = smallestFeature)
            rectColor = (0, 0, 255)
        eyes = []
        for (x, y, w, h) in faces:
            x = x - 100//cvScaleFactor
            y = y - 100//cvScaleFactor
            w = w + 100//cvScaleFactor
            h = h + 100//cvScaleFactor
            justFaceGray = gray[x:(x+w+1),y:(y+h+1)]
            eyes = eyes_cascade.detectMultiScale(justFaceGray, 1.08)
            for eye in eyes:
                eye[0] = eye[0] + y
                eye[1] = eye[1] + x
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(editedFrame, (cvScaleFactor*x, cvScaleFactor*y), (cvScaleFactor*(x+w), cvScaleFactor*(y+h)), rectColor, 4)
        # Draw rectangle around the eyes
        for (x, y, w, h) in eyes:
            cv2.rectangle(editedFrame, (cvScaleFactor*x, cvScaleFactor*y), (cvScaleFactor*(x+w), cvScaleFactor*(y+h)), (200, 200, 200), 2)
        if len(eyes) == 2:
            for (x, y, w, h) in eyes:
                radius = (w+h)//2
                cv2.circle(editedFrame, (cvScaleFactor*(x+w//2), cvScaleFactor*(y+h//2)), radius, (20, 20, 0), 2)
                cv2.circle(editedFrame, (cvScaleFactor*(x+w//2), cvScaleFactor*(y+h//2)), radius, (20, 20, 0), 2)
            
        

            
        
        
        #format the frame for the camera output, adding a 4th channel
        editedFrame4ch = np.ones((cam.height, cam.width, 4), np.uint8)*255 # RGBA
        editedFrame4ch[:, :, 0:3] = cv2.cvtColor(editedFrame, cv2.COLOR_BGR2RGB)
        
        cam.send(editedFrame4ch)

        fpsList.append(time.time() - startOfFrame)
        #cam.sleep_until_next_frame()

cap.release()
fpsList[0] = fpsList[1]
print("Min  FPS: {}".format(1/max(fpsList)))
print("Mean FPS: {}".format(1/mean(fpsList)))
print("Max  FPS: {}".format(1/min(fpsList)))
