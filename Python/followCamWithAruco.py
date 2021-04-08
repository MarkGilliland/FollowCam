import pyvirtualcam # https://github.com/letmaik/pyvirtualcam
import numpy as np #pip install numpy
from cv2 import aruco
import cv2 #pip install opencv-contrib-python
import time
from statistics import mean
from math import sqrt

import custom_serial_tools as ardLib#Uses pyserial custom_serial_tools.py should be located in the same dir as this file
ser = ardLib.initGimbal(useFirstFound=True)

#Init Aruco marker things, see also https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/aruco_basics.html
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)
aruco_parameters =  aruco.DetectorParameters_create()

cap = 0
i = 0
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

debugDrawings = False
arucoOnly = True

movementDeadband = (0.2, 0.12)#as ratio of full screen size, ish
movementGain = 0.02
neutralX = -0.4
neutralY = -0.4
posX = neutralX
posY = neutralY

arucoScaleFactor = 2.0
arucoImgWidth = int(capWidth/arucoScaleFactor)
arucoImgHeight = int(capHeight/arucoScaleFactor)

faceDetectionScaleFactor = 6.0
faceDetectionImgWidth = int(capWidth/faceDetectionScaleFactor)
faceDetectionImgHeight = int(capHeight/faceDetectionScaleFactor)
smallestFeature = tuple([int(minFaceSize//faceDetectionScaleFactor)])*2

centerFace = [capWidth/(2*faceDetectionScaleFactor)-25,  capHeight/(2*faceDetectionScaleFactor)-25,  50,  50]
historyLen = 3
featureCenterHistX = [neutralX]*historyLen
featureCenterHistY = [neutralY]*historyLen
lastFace = centerFace
lastFaceTimestamp = time.time()


fpsList = [0.03]

with pyvirtualcam.Camera(width=capWidth, height=capHeight, fps=30, delay = 0) as cam:
    print("Virtual cam connected")
    ardLib.startingAnimation(ser)
    time.sleep(0.2)
    progStart = time.time()
    #while(time.time() - progStart < 60):
    while(True):
        startOfFrame = time.time()
        # Read the input image
        ret, capFrame = cap.read()
        editedFrame = capFrame
        #Make it grayscale
        grayCapFrame = cv2.cvtColor(capFrame, cv2.COLOR_BGR2GRAY)

        #Resize for aruco markers
        grayForAruco = cv2.resize(grayCapFrame, (arucoImgWidth, arucoImgHeight))

        #Find the aruco
        arucoCorners, arucoIds, rejectedImgPoints = aruco.detectMarkers(grayForAruco, aruco_dict, parameters=aruco_parameters)
        arucoFound = arucoIds is not None
        arucoIndex = 0
        if arucoFound:
            arucoIndex = arucoIds.argmin()
            arucoIndex = 0
            arucoCenters = arucoCorners[arucoIndex].mean(axis=1)
            lastFaceTimestamp = time.time()

        #if no aruco found, then look for faces
        if(not arucoFound and not arucoOnly):
            gray = cv2.resize(grayCapFrame, (faceDetectionImgWidth, faceDetectionImgHeight))
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

            if len(faces) > 0:#if a face was actually found
                lastFaceTimestamp = time.time()
                
            else:
                faces = [lastFace]
                rectColor = (100, 100, 100)

            if lastFaceTimestamp + 1.5 < time.time():
                faces = [centerFace]
                rectColor = (50, 100, 200)
            if lastFaceTimestamp + 7 < time.time():
                posX = neutralX
                posY = neutralY
                rectColor = (0, 0, 0)
            #Pick the best face
            faceSizes = []
            #centerDists = []
            for faceInd in range(len(faces)):
                x, y, w, h = faces[faceInd]
                faceSizes.append([faceInd, w*h])
                #centerDist.append([faceIndsqrt(x*x + y*y)])
            faceSizes = sorted(faceSizes, key=lambda size: size[1])
        elif arucoOnly:
            faces = []

        
        
        
        # Draw rectangle around the favorite face
        featureCenter = (0,0)
        if arucoFound:
            featureCenter = tuple([int(arucoCenters[0][0]*arucoScaleFactor), int(arucoCenters[0][1]*arucoScaleFactor)])
            w = 200
            rectColor = (200, 100, 50)
            scaleFactor = arucoScaleFactor
            faceSizes = [[0]]
            faces = [0]
            faces[faceSizes[0][0]] = (int(arucoCenters[0][0]*arucoScaleFactor/faceDetectionScaleFactor), int(arucoCenters[0][1]*arucoScaleFactor/faceDetectionScaleFactor), 100, 100)
        if not arucoFound and len(faces) > 0:
            x, y, w, h = faces[faceSizes[0][0]]
            #cv2.rectangle(editedFrame, (int(faceDetectionScaleFactor*x), int(faceDetectionScaleFactor*y)), (int(faceDetectionScaleFactor*(x+w)), int(faceDetectionScaleFactor*(y+h))), rectColor, 4)
            featureCenter = (int(faceDetectionScaleFactor*(x+w/2)), int(faceDetectionScaleFactor*(y+h/2)))
            scaleFactor = faceDetectionScaleFactor

        if arucoFound or len(faces) > 0:
            if debugDrawings:
                cv2.circle(editedFrame, featureCenter, int(scaleFactor*w / 15), rectColor, 3)

            featureX = (featureCenter[0] - capWidth*0.5) / (capWidth*0.5)
            featureY = (featureCenter[1] - capHeight*0.5) / (capHeight*0.5)


            featureCenterHistX.append(featureX)#add the newest
            featureCenterHistX.pop(0)#remove the oldest
            featureCenterHistY.append(featureY)#add the newest
            featureCenterHistY.pop(0)#remove the oldest

            filteredfeatureX = sum(featureCenterHistX)/len(featureCenterHistX)
            filteredfeatureY = sum(featureCenterHistY)/len(featureCenterHistY)

            if abs(filteredfeatureX) > movementDeadband[0]:
                posX += -1.0*filteredfeatureX * movementGain
            if abs(filteredfeatureY) > movementDeadband[1]:
                posY += -1.0*filteredfeatureY * movementGain

            posX,posY = ardLib.writeNewPos(ser, posX, posY)
                
            lastFace = faces[faceSizes[0][0]]

        #Draw deadband zone
        #cv2.rectangle(editedFrame, (capWidth/2 - movementDeadband[0]*capWidth,  capHeight/2 - movementDeadband[1]*capHeight), (capWidth/2 + movementDeadband[0]*capWidth,  capHeight/2 + movementDeadband[1]*capHeight), (0, 0, 50), 5)
        #corner1 = (int(capWidth/2 - movementDeadband[0]*capWidth),  int(capHeight/2 - movementDeadband[1]*capHeight))
        #corner2 = (int(capWidth/2 + movementDeadband[0]*capWidth),  int(capHeight/2 + movementDeadband[1]*capHeight))
        #rectColor = (0, 0, 0)
        #cv2.rectangle(editedFrame, corner1, corner2, rectColor, 5)
        
        #format the frame for the camera output, adding a 4th channel
        editedFrame4ch = np.ones((cam.height, cam.width, 3), np.uint8)*255 # RGBA
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
