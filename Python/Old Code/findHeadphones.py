import numpy as np
import cv2
from math import sqrt
#headphoneColorHSV = (142, 240, 163)
headphoneLowEdge = np.array([10, 160, 100], np.uint8)
headphoneHighEdge = np.array([160, 255, 255], np.uint8)

def findHeadphones(img):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, headphoneLowEdge, headphoneHighEdge)

    mask = cv2.blur(mask, (20,20))

    contours, heirarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    contours.sort(reverse=True, key=cv2.contourArea)

    bigContourRects = []

    bigContourCents = []
    
    headEstimate = [0, 0, 0]#Center of the headphones, radius of the approx right size
    
    if len(contours) >= 2 and cv2.contourArea(contours[1]) > 1500:
        for i in range(min(len(contours),2)):
            cont = contours[i]
            boundingRect = cv2.boundingRect(cont)
            bigContourRects.append(boundingRect)

            mom = cv2.moments(cont)
            cent = (mom['m10']/mom['m00'] , mom['m01']/mom['m00'])

            bigContourCents.append(cent)

            headEstimate[0] += int(cent[0]/2)
            headEstimate[1] += int(cent[1]/2)

        headEstimate[2] = int(sqrt((bigContourCents[0][0] - bigContourCents[1][0])**2 + (bigContourCents[0][1] - bigContourCents[1][1])**2)*0.8)


    return [bigContourRects, headEstimate]
