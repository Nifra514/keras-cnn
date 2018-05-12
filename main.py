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
# import tutorial

class login(QtWidgets.QMainWindow):
    def __init__(self):
        super(login,self).__init__()
        loadUi('UI/login.ui',self)
        self.btn_login.clicked.connect(self.on_login)

    def messagebox(self,title,message):
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle(title)
        msgbox.setText(message)
        msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgbox.exec_()
        
    def clear(self):
        self.txt_uname.setText("")
        self.txt_password.setText("")


    def on_login(self):
        
        connect = pymysql.connect(host='localhost', user='root', password='',db='asl')

        uname = self.txt_uname.text()
        password = self.txt_password.text()

        pw = password.encode("utf-8")
        hash = hashlib.md5(pw)
        pword = hash.hexdigest()   

        con = connect.cursor()
        sql = "SELECT * FROM user_details WHERE username = '%s' AND password = '%s'"%(uname,pword)
        
        con.execute(sql)
        result = con.fetchall()

        if (len(result) > 0):
            # self.Messagebox('invalid','invalid')
            # for r in result:           
                # if (r[4] == uname and r[5] == pword):
            self.main = main()
            self.main.show()
            self.hide()
                # else:
                #     print("Login Error") 
        else:            
            self.messagebox('Invalid Login','Invalid Username or Password!!!')
            self.clear()

class main(QtWidgets.QMainWindow):
    def __init__(self):
        super(main,self).__init__()
        loadUi('UI/main.ui',self)    
        self.btn_exam.clicked.connect(self.on_exam)
        self.btn_exit.clicked.connect(self.on_exit)
        self.btn_tut.clicked.connect(self.on_tut)

    def on_exam(self):
        self.ex = exam()
        self.ex.show()
        self.hide()

    def on_exit(self):
        self.lg = login()
        self.lg.show()
        self.hide()

    def on_tut(self):
        os.system('tutorial.py')
        

class exam(QtWidgets.QMainWindow):
    def __init__(self):
        super(exam,self).__init__()
        loadUi('UI/exam.ui',self)     
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(10)
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,720)

        self.timer1 = QtCore.QTimer(self)
        self.timer1.timeout.connect(self.update_frame)
        self.timer1.start(5)
        self.btn_snap.clicked.connect(self.snap)

    def update_time(self):
        # self.q_lcdn.display(QtCore.QTime.currentTime().toString())
        self.lbl_time.setText(QtCore.QTime.currentTime().toString())
        self.lbl_date.setText(QtCore.QDate.currentDate().toString())

    # def start_cam(self):
    #     self.cap = cv2.VideoCapture(0)
    #     self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
    #     self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,720)

    #     self.timer1 = QtCore.QTimer(self)
    #     self.timer1.timeout.connect(self.update_frame)
    #     self.timer1.start(5)

    def update_frame(self):
        ret, self.image = self.cap.read()
        self.image = cv2.flip(self.image, 1)

        if ret:                
            x1, y1, x2, y2 = 20, 20, 220, 270
            cv2.rectangle(self.image, (x1, y1), (x2, y2), (0,0,255), 1)

        self.displayImage(self.image, 1)
        
    def snap(self):
        self.x1,self.y1,self.x2,self.y2 = 20, 20, 220, 270
        img_cropped = self.image[self.y1:self.y2, self.x1:self.x2] 
        cv2.imwrite('predict/capture.jpg', img_cropped)

        bpath = os.getcwd()
        fpath = 'predict'
        path = os.path.join(bpath,fpath,'capture.jpg')

        self.lbl_img_snap.setPixmap(QtGui.QPixmap(path))
        self.lbl_img_snap.show()

        # os.system('predictor.py')        

        from keras.models import Sequential
        from keras.layers import Conv2D, MaxPooling2D
        from keras.layers import Activation, Dropout, Flatten, Dense
        from keras import backend as K
        from keras.preprocessing import image
        

        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

        # dimensions of our images
        img_width, img_height = 150, 150

        if K.image_data_format() == 'channels_first':
            input_shape = (3, img_width, img_height)
        else:
            input_shape = (img_width, img_height, 3)

        names = {
            0 : 'A',
            1 : 'B',
            2 : 'C',
            3 : 'D',
            4 : 'E',
            5 : 'F',
            6 : 'G',
            7 : 'H',
            8 : 'I',
            9 : 'J',
            10: 'K',
            11: 'L',
            12: 'M',
            13: 'N',
            14: 'O',
            15: 'P',
            16: 'Q',
            17: 'R',
            18: 'S',
            19: 'T',
            20: 'U',
            21: 'V',
            22: 'W',
            23: 'X',
            24: 'Y',
            25: 'Z',
            # 26: '1',
            # 27: '2',
            # 28: '3',
            # 29: '4',
            # 30: '5',
            # 31: '6',
            # 32: '7',
            # 33: '8',
            # 34: '9',
            
        }

        bpath = os.getcwd()
        fpath = 'predict'
        path = os.path.join(bpath,fpath,'capture.jpg')

        # if path == '':
        #     print (path)
        #     sys.exit()
        # else:
        _dir =  str(path)

        #input
        model = Sequential()
        model.add(Conv2D(32, (3, 3), input_shape=input_shape,padding='same'))
        model.add(Dropout(0.2))
        #model.add(MaxPooling2D(pool_size=(2, 2)))

        #first convo
        model.add(Conv2D(32, (3, 3), padding='valid'))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))

        #second convo
        model.add(Conv2D(64, (3, 3), padding='valid'))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))

        #third convo
        model.add(Conv2D(64, (3, 3), padding='valid'))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))

        #fully connected
        model.add(Flatten())
        model.add(Dense(256))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(26))
        model.add(Activation('softmax'))

        #load model 
        model.load_weights('./models/trained_model_3.h5')

        model.compile(loss='categorical_crossentropy',
                    optimizer='adam',
                    metrics=['categorical_accuracy'])


        # dir_files = glob.glob(_dir+'*.jpg')

        # for _file in dir_files:
        #     file_path = _file
            

        img = image.load_img(_dir, target_size=(img_width, img_height))

        x = image.img_to_array(img)

        x = np.expand_dims(x, axis=0)

        images = np.vstack([x])

        # classes = model.predict(images)

        p_classes = model.predict_classes(images)
        # print (p_classes)
        letter = names[p_classes[0]]
        print (letter)
        self.lbl_ans.setText(letter)


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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    lg = login()
    lg.show()
    sys.exit(app.exec_())





