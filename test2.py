import datetime
import os
import numpy as np 
import cv2 


bpath = os.getcwd()
fpath = 'predict'
path = os.path.join(bpath,fpath,'3_65' + '.jpg')

# frame1 = cv2.imread (path)
cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=100, detectShadows=False)

while True:
   
    ret, frame  = cap.read()
    frame1 = cv2.flip(frame, 1)
    

    fgmask = fgbg.apply(frame1)

    # grayscaled = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY) 
    # gaus = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,115,1) 
    # edges = cv2.Canny(fgmask, 100,200)
    cv2.imshow("mask", fgmask)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cv2.destroyAllWindows()



# cap = cv2.VideoCapture(0)
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
# fgbg = cv2.createBackgroundSubtractorMOG2(history=0, varThreshold=0, detectShadows=False)

# while True:
#     ret, frame  = cap.read()
#     frame = cv2.flip(frame, 1)
#     fgmask = fgbg.apply(frame)
#     fgthres = cv2.threshold(fgmask.copy(), 25, 255, cv2.THRESH_BINARY)[1]
#     # fgdilated = cv2.dilate(fgthres, kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)), iterations = 3)
#     fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    
#     cv2.imshow('windowNameFG1',fgthres)
#     # cv2.imshow('windowNameFG2',fgdilated)
#     cv2.imshow('windowNameFGP',fgmask)


#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         break

cap.release()
cv2.destroyAllWindows()

