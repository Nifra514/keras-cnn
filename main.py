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
import webbrowser
import datetime
import requests
import json
import utility
import pickledb


class loading(QtWidgets.QMainWindow):
    def __init__(self):
        super(loading,self).__init__()
        loadUi('UI/load.ui',self)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.test_connection)
        self.timer.start(10)

    def messagebox(self,title,message):
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle(title)
        msgbox.setText(message)
        msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgbox.exec_()

        
    def test_connection(self):
        connection = utility.check_internet()
        if connection == 200:            
            self.step = 0
            while self.step < 100:
                self.step += 0.0001
                self.q_pb.setValue(self.step)

            self.lg = login()
            self.lg.show()
            self.hide()
            self.timer.disconnect()
            
        else:  
            conection_error= str(connection)
            self.messagebox('Connection Error',conection_error)
            sys.exit()
            
        
class login(QtWidgets.QMainWindow):
    def __init__(self):
        super(login,self).__init__()
        loadUi('UI/login.ui',self)
        self.btn_login.clicked.connect(self.on_login)
        self.btn_reg.clicked.connect(self.on_reg)
        self.btn_exit.clicked.connect(self.on_exit)

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
        
        # connect = pymysql.connect(host='localhost', user='root', password='',db='asl')

        uname = self.txt_uname.text()
        password = self.txt_password.text()

        # pw = password.encode("utf-8")
        # hash = hashlib.md5(pw)
        # pword = hash.hexdigest()   

        # con = connect.cursor()
        # sql = "SELECT * FROM user_details WHERE username = '%s' AND password = '%s'"%(uname,pword)
        
        # con.execute(sql)
        # result = con.fetchall()
        
        #api login
        token = utility.make_login(uname, password)
        print("RECIVED TOKEN %s", (token))
        

        if (token["status"] == True):
            #save token
            utility.set_token(token["data"])
            self.main = main()
            self.main.show()
            self.hide()
            
        else:   
            self.messagebox('Invalid Login',token['data'])
            self.clear()

        

    def on_reg(self):
        webbrowser.open('http://localhost:8888/asllearning/Views/registration.php')

    def on_exit(self):
        sys.exit()

class main(QtWidgets.QMainWindow):
    def __init__(self):
        super(main,self).__init__()
        loadUi('UI/main.ui',self)    
        
        self.btn_pred.clicked.connect(self.on_pred)
        self.btn_exit.clicked.connect(self.on_exit)
        self.btn_tut.clicked.connect(self.on_tut)
        info = utility.user_info()
        self.lbl_name.setText(info['u_name'])
        

    def on_pred(self):
        self.prediction = prediction()
        self.prediction.show()
        self.hide()

    def on_exit(self):
        sys.exit()

    def on_tut(self):
        os.system('tutorial.py')
        

class prediction(QtWidgets.QMainWindow):
    def __init__(self):
        super(prediction,self).__init__()
        loadUi('UI/prediction.ui',self)    

        info = utility.user_info()
        self.lbl_name.setText(info['u_name'])

        self.timer1 = QtCore.QTimer()
        self.timer1.timeout.connect(self.update_time)
        self.timer1.start(10)
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,720)

        self.timer2 = QtCore.QTimer(self)
        self.timer2.timeout.connect(self.update_frame)
        self.timer2.start(5)
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
            cv2.rectangle(self.image, (x1, y1), (x2, y2), (0,0,255), 1)

        self.displayImage(self.image, 1)
        
    def snap(self):

        # nam = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

        self.x1,self.y1,self.x2,self.y2 = 20, 20, 220, 270
        img_cropped = self.image[self.y1:self.y2, self.x1:self.x2] 
        cv2.imwrite('preview/capture.jpg', img_cropped)
        # cv2.imwrite('preview/capture' +  str(nam) + '.jpg', img_cropped)

        bpath = os.getcwd()
        fpath = 'preview'
        path = os.path.join(bpath,fpath,'capture.jpg')

        self.lbl_img_snap.setPixmap(QtGui.QPixmap(path))
        self.lbl_img_snap.show()

        imgs = cv2.imread(path)
        edges = cv2.Canny(imgs, 100,200)
        # cv2.imshow("edges", edges)
        cv2.imwrite('predict/capture.jpg', edges)
        
        bpath = os.getcwd()
        fpath = 'predict'
        path1 = os.path.join(bpath,fpath,'capture.jpg')
        
        # CNN Predictor Code Block

        from keras.models import Sequential
        from keras.layers import Conv2D, MaxPooling2D
        from keras.layers import Activation, Dropout, Flatten, Dense
        from keras import backend as K
        from keras.preprocessing import image
        from keras.optimizers import Adam
        

        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

        # dimensions of our images
        img_width, img_height = 200, 250

        if K.image_data_format() == 'channels_first':
            input_shape = (3, img_width, img_height)
        else:
            input_shape = (img_width, img_height, 3)

        names = {
            0: '1',
            1: '2',
            2: '3',          
            
        }

        # if path == '':
        #     print (path)
        #     sys.exit()
        # else:

        _dir =  str(path1)
        
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

        #fourth convo
        model.add(Conv2D(128, (3, 3), padding='valid'))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))

        #fifth convo
        model.add(Conv2D(128, (3, 3), padding='valid'))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))

        #fully connected
        model.add(Flatten())
        model.add(Dense(256))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(3))
        model.add(Activation('softmax'))

        #load model 
        model.load_weights('./models/trained_model3.h5')

        model.compile(loss='categorical_crossentropy',
                    optimizer=Adam(lr=1e-3),
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
        # End Of CNN Predictor Code Block

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
        self.mn = main()
        self.mn.show()
        self.hide()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # lg = login()
    # lg.show()
    ld = loading()
    ld.show()
    sys.exit(app.exec_())





