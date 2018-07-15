import sys
import os
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
from PyQt5.uic import loadUi
import pymysql
import hashlib
import numpy as np
import cv2
import tutorial
import datetime


        

class prediction(QtWidgets.QMainWindow):
    def __init__(self):
        super(prediction,self).__init__()
        loadUi('UI/prediction.ui',self)     
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(10)
        # self.btn_start.clicked.connect(self.start_cam)
        # self.btn_snap.setCheckable(True)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,720)

        self.timer1 = QtCore.QTimer(self)
        self.timer1.timeout.connect(self.update_frame)
        self.timer1.start(5)
        self.btn_snap.clicked.connect(self.snap)
        self.btn_exit.clicked.connect(self.exit)

    def update_time(self):
        # self.q_lcdn.display(QtCore.QTime.currentTime().toString())
        self.lbl_time.setText(QtCore.QTime.currentTime().toString())
        self.lbl_date.setText(QtCore.QDate.currentDate().toString())

    
    def update_frame(self):
        
        ret, self.image = self.cap.read()            
        self.image = cv2.flip(self.image, 1)   

        if ret:                
            x1, y1, x2, y2 = 20, 20, 220, 270
            cv2.rectangle(self.image, (x1, y1), (x2, y2), (0,0,250), 1)
        
        self.displayImage(self.image, 1)
        
        
               
    def snap(self):
        
        i = 0
        while i in range(150): 
        
        
            self.x1,self.y1,self.x2,self.y2 = 20, 20, 220, 270
            img_cropped = self.image[self.y1:self.y2, self.x1:self.x2] 
            i+=1
            name = str(i) 
            cv2.imwrite('data_set/'+ name + '.jpg', img_cropped)

            bpath = os.getcwd()
            fpath = 'data_set/'
            path = os.path.join(bpath,fpath,name + '.jpg')

            img = cv2.imread(path)
            
            # grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
            # gaus = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,115,1) 
            edges = cv2.Canny(img, 100,200)


            cv2.imwrite('Dataset/train/' +  name + '.jpg', edges)

            # os.remove(path)
        
        

    def displayImage(self, img, window=1):
        qformat = QtGui.QImage.Format_Indexed8
        if len(img.shape)==3:
            if img.shape[2]==4:
                qformat = QtGui.QImage.Format_RGBA8888
            else:
                qformat = QtGui.QImage.Format_RGB888

        outImage = QtGui.QImage(
            img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.lbl_cam.setPixmap(QtGui.QPixmap.fromImage(outImage))
            self.lbl_cam.setScaledContents(True)

    def exit(self):
        sys.exit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # lg = login()
    # lg.show()
    prediction = prediction()
    prediction.show()
    sys.exit(app.exec_())





