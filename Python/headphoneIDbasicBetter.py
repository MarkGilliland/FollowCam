import numpy as np
import cv2
import time

desiredColorHSV = (142, 240, 163)
#desiredColor = (91, 195, 255)

img = cv2.imread('testImgFrontFace.png')

tic = time.time()
imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
lowEdge = np.array([10, 160, 100], np.uint8)
highEdge = np.array([160, 255, 255], np.uint8)
mask = cv2.inRange(imgHSV, lowEdge, highEdge)
print(time.time()-tic)


cv2.imshow('most-blue version', mask)
##imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
##ret,thresh = cv2.threshold(imgray,127,255,0)
##image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
