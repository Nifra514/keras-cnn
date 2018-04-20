import sys
import cv2
import matplotlib.pyplot as plt
import numpy as np
import PyQt5
#from PyQt5.QtWidgets import QtCore, QApplication, QDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class cam(QtWidgets.QDialog):
    def __init__(self):
        super(cam, self).__init__()
        loadUi('cam.ui', self)

        self.btn_start.clicked.connect(self.start_webcam)
        self.btn_stop.clicked.connect(self.stop_webcam)
        # self.btn_snap.clicked.connect(self.capturev)

    # def capturev(self):
    #     capture=cv2.VideoCapture(0)

    #     while(True):
    #         ret, frame = capture.read()
    #         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    #         cv2.imshow('frame', rgb)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             out = cv2.imwrite('capture.jpg', frame)
    #             break

    #     capture.release()
    #     cv2.destroyAllWindows()


    def start_webcam(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        ret, self.image = self.capture.read()
        self.image = cv2.flip(self.image, 1)
        self.displayImage(self.image, 1)

    def stop_webcam(self):
        self.timer.stop()
    # sys.exit()
    def displayImage(self, img, window=1):
        qformat = QtGui.QImage.Format_Indexed8
        if (len(img.shape)==3):
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

    # def capturev(self):
    #     cap=cv2.VideoCapture(0)

    #     if cap.isOpened():
    #         ret, frame = cap.read()
    #         print(ret)
    #         print(frame)
    #     else:
    #         ret = False
    #         img1 = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    #         plt.imshow(img1)
    #         plt.xticks([])
    #         plt.yticks([])
    #         plt.show()

    #         cap.release()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = cam()
    window.setWindowTitle('camtut')
    window.show()
    sys.exit(app.exec_())
