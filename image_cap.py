import sys
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import cv2
       

class image_cap(QtWidgets.QMainWindow):
    def __init__(self):
        super(image_cap,self).__init__()
        loadUi('UI/image_cap.ui',self)     
    
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,720)

        self.timer1 = QtCore.QTimer(self)
        self.timer1.timeout.connect(self.update_frame)
        self.timer1.start(5)
        self.btn_snap.clicked.connect(self.snap)
        self.btn_back.clicked.connect(self.back)

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

            cv2.imwrite('data_set/1/'+ name + '.jpg', img_cropped)

            edges = cv2.Canny(img_cropped, 75,150)

            cv2.imwrite('Dataset/train/1/' +  name + '.jpg', edges)     
        

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

    def back(self):
        sys.exit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    image_cap = image_cap()
    image_cap.show()
    sys.exit(app.exec_())





