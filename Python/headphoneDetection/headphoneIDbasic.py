import numpy as np
import cv2

desiredColorHSV = (142, 240, 163)
desiredColor = (91, 195, 255)

img = cv2.imread('testImgFrontFace.png')
imgMatch = np.zeros(img.shape)
for i in range(len(imgMatch)):
    for j in range(len(imgMatch[i])):
        imgHSV[i][j][0] = 
        imgHSV[i][j][1] = 
        imgHSV[i][j][2] = 
        

cv2.imshow('most-blue version', imgMatch)
##imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
##ret,thresh = cv2.threshold(imgray,127,255,0)
##image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
