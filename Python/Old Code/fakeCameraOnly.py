import pyvirtualcam # https://github.com/letmaik/pyvirtualcam
import numpy as np #pip install numpy
import cv2 #pip install opencv-python

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

with pyvirtualcam.Camera(width=1280, height=720, fps=15) as cam:
    while(True):
        ret, capFrame = cap.read()

        editedFrame = capFrame

        #format the frame for the camera output, adding a 4th channel
        editedFrame4ch = np.ones((cam.height, cam.width, 4), np.uint8)*255 # RGBA
        editedFrame4ch[:, :, 0:3] = cv2.cvtColor(editedFrame, cv2.COLOR_BGR2RGB)
        
        cam.send(editedFrame4ch)
        cam.sleep_until_next_frame()

cap.release()
