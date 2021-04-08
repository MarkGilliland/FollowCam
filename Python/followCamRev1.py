import pyvirtualcam # https://github.com/letmaik/pyvirtualcam
import numpy as np #pip install numpy
import cv2 #pip install opencv-python
import time
from statistics import mean
from math import sqrt

import custom_serial_tools as ardLib

ser = ardLib.initGimbal(useFirstFound=True)


#import custom_serial_tools as ardLib #Stuff to move the gimbal

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


movementDeadband = (0.25, 0.15)#as ratio of full screen size, ish
movementGain = 0.025
posX = 0
posY = 0

cvScaleFactor = 4
cvWidth = int(capWidth/cvScaleFactor)
cvHeight = int(capHeight/cvScaleFactor)
smallestFeature = tuple([int(minFaceSize//cvScaleFactor)])*2

centerFace = [capWidth/(2*cvScaleFactor)-25,  capHeight/(2*cvScaleFactor)-25,  50,  50]
lastFace = centerFace
lastFaceReuse = 0


fpsList = [0.03]

with pyvirtualcam.Camera(width=capWidth, height=capHeight, fps=20, delay = 0) as cam:
    print("Virtual cam connected")
    ardLib.startingAnimation(ser)
    time.sleep(0.2)
    posY += -0.2
    progStart = time.time()
    while(time.time() - progStart < 60):
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
        rectColor = (100, 0, 0)
        if len(faces) == 0:
            faces = secondary_cascade.detectMultiScale(gray, 1.1, minSize = smallestFeature)
            rectColor = (0, 100, 0)
        if len(faces) == 0:
            faces = tertiary_cascade.detectMultiScale(gray, 1.1, minSize = smallestFeature)
            rectColor = (0, 0, 100)

        if len(faces) == 0:
            faces = [lastFace]
            rectColor = (100, 100, 100)
            lastFaceReuse += 1
        else:
            lastFaceReuse = 0

        if lastFaceReuse > cam.fps*1.5:
            faces = [centerFace]

        #Pick the best face
        faceSizes = []
        #centerDists = []
        for faceInd in range(len(faces)):
            x, y, w, h = faces[faceInd]
            faceSizes.append([faceInd, w*h])
            #centerDist.append([faceIndsqrt(x*x + y*y)])
        faceSizes = sorted(faceSizes, key=lambda size: size[1])
        
        # Draw rectangle around the favorite face
        if len(faces) > 0:
            x, y, w, h = faces[faceSizes[0][0]]
            #cv2.rectangle(editedFrame, (cvScaleFactor*x, cvScaleFactor*y), (cvScaleFactor*(x+w), cvScaleFactor*(y+h)), rectColor, 4)
            faceCenter = (int(cvScaleFactor*(x+w/2)), int(cvScaleFactor*(y+h/2)))
            cv2.circle(editedFrame, faceCenter, int(cvScaleFactor*w / 8), rectColor, 5)

            faceX = (faceCenter[0] - capWidth*0.5) / (capWidth*0.5)
            faceY = (faceCenter[1] - capHeight*0.5) / (capHeight*0.5)

            if abs(faceX) > movementDeadband[0]:
                posX += -1.0*faceX * movementGain
            if abs(faceY) > movementDeadband[1]:
                posY += -1.0*faceY * movementGain

            posX,posY = ardLib.writeNewPos(ser, posX, posY)
                
        lastFace = faces[0]

        #Draw deadband zone
        #cv2.rectangle(editedFrame, (capWidth/2 - movementDeadband[0]*capWidth,  capHeight/2 - movementDeadband[1]*capHeight), (capWidth/2 + movementDeadband[0]*capWidth,  capHeight/2 + movementDeadband[1]*capHeight), (0, 0, 50), 5)
        #corner1 = (int(capWidth/2 - movementDeadband[0]*capWidth),  int(capHeight/2 - movementDeadband[1]*capHeight))
        #corner2 = (int(capWidth/2 + movementDeadband[0]*capWidth),  int(capHeight/2 + movementDeadband[1]*capHeight))
        #rectColor = (0, 0, 0)
        #cv2.rectangle(editedFrame, corner1, corner2, rectColor, 5)
        
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
##Close the port when done
ser.close()
