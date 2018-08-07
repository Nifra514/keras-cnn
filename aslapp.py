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

with open('config/config.json') as json_data:
    jsd = json.load(json_data)

class loading(QtWidgets.QMainWindow):
    def __init__(self):
        super(loading, self).__init__()
        loadUi('UI/load.ui', self)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.test_connection)
        self.timer.start(10)

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
            conection_error = str(connection)
            QtWidgets.QMessageBox.warning(
                self, 'Connection Error', conection_error)
            sys.exit()


class login(QtWidgets.QMainWindow):
    def __init__(self):
        super(login, self).__init__()
        loadUi('UI/login.ui', self)
        self.btn_login.clicked.connect(self.on_login)
        self.btn_reg.clicked.connect(self.on_register)
        self.btn_exit.clicked.connect(self.on_exit)

    def clear(self):
        self.txt_uname.setText("")
        self.txt_password.setText("")

    def on_login(self):

        connection = utility.check_internet()
        if connection == 200:

            uname = self.txt_uname.text()
            password = self.txt_password.text()

            # api login
            token = utility.make_login(uname, password)
            # print("RECIVED TOKEN %s", (token))

            if (token["status"] == True):
                # save token
                utility.set_token(token["data"])
                self.main = main()
                self.main.show()
                self.hide()

            else:
                QtWidgets.QMessageBox.critical(
                    self, 'Invalid Login', token['data'])
                self.clear()

        else:
            conection_error = str(connection)
            QtWidgets.QMessageBox.warning(
                self, 'Connection Error', conection_error)
            sys.exit()

    def on_register(self):
        webbrowser.open(
            'http://asllearning.info/Views/registration.php')

    def on_exit(self):
        sys.exit(0)


class main(QtWidgets.QMainWindow):
    def __init__(self):
        super(main, self).__init__()
        loadUi('UI/main.ui', self)

        # Download model from server and save to local folder
        utility.download_model()

        self.btn_pred.clicked.connect(self.on_predictor)
        self.btn_logout.clicked.connect(self.on_logout)
        self.btn_tut.clicked.connect(self.on_tutorial)

        self.info = utility.user_info()
        self.lbl_name.setText(self.info['u_name'])

        

    def on_predictor(self):

        try:
            self.prediction = prediction()
            self.prediction.show()
            self.hide()
            
            user_id = self.info['id']
            log_type = jsd["lg_log"]
            log_data = "User: "+self.info['id']+" loading predictor"
            action = "Load Predictor"
            risk = jsd["rsk_none"]

            utility.write_log(user_id, log_type, log_data, action, risk)

        except:

            QtWidgets.QMessageBox.critical(
                self, 'Error', "Error Loading Predictor. Please Try Again Later!!!")

            user_id = jsd["system"]
            log_type = jsd["lg_error"]
            log_data = "Error loading predictor for user: "+self.info['id']
            action = "Load Predictor"
            risk = jsd["rsk_high"]

            utility.write_log(user_id, log_type, log_data, action, risk)

    def on_tutorial(self):
        try:

            user_id = self.info['id']
            log_type = jsd["lg_log"]
            log_data = "User: "+self.info['id']+" loading tutorial"
            
            action = "Load Tutorial"
            risk = jsd["rsk_none"]

            utility.write_log(user_id, log_type, log_data, action, risk)

            os.system('tutorial.py')

        except:
            QtWidgets.QMessageBox.warning(
                self, 'Warning', "Unable To Load Tutorial At The Moment. Please Try Again Later!!!")
            user_id = jsd["system"]
            log_type = jsd["lg_warning"]
            log_data = "Unable to load tutorial for user: "+self.info['id']
            action = "Load Tutorial"
            risk = jsd["rsk_low"]

            utility.write_log(user_id, log_type, log_data, action, risk)

    def on_logout(self):

        user_id = self.info['id']
        log_type = jsd["lg_log"]
        log_data = "User "+self.info['id'] + \
            " logged out from ASLapp successfully"
        action = "Logout"
        risk = jsd["rsk_none"]

        utility.write_log(user_id, log_type, log_data, action, risk)

        self.lg = login()
        self.lg.show()
        self.close()
        utility.logout()


class prediction(QtWidgets.QMainWindow):
    def __init__(self):
        super(prediction, self).__init__()
        loadUi('UI/prediction.ui', self)

        self.info = utility.user_info()
        self.lbl_name.setText(self.info['u_name'])

        self.timer1 = QtCore.QTimer()
        self.timer1.timeout.connect(self.update_time)
        self.timer1.start(10)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)

        self.timer2 = QtCore.QTimer(self)
        self.timer2.timeout.connect(self.update_frame)
        self.timer2.start(5)
        self.btn_snap.clicked.connect(self.snap)
        self.btn_back.clicked.connect(self.back)

    def update_time(self):
        # self.q_lcdn.display(QtCore.QTime.currentTime().toString())
        self.lbl_time.setText(QtCore.QTime.currentTime().toString())
        self.lbl_date.setText(QtCore.QDate.currentDate().toString())

    def update_frame(self):
        ret, self.image = self.cap.read()
        self.image = cv2.flip(self.image, 1)

        if ret:
            x1, y1, x2, y2 = 20, 20, 220, 270
            cv2.rectangle(self.image, (x1, y1), (x2, y2), (0, 0, 255), 1)

        self.displayImage(self.image, 1)

    def displayImage(self, img, window=1):
        qformat = QtGui.QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QtGui.QImage.Format_RGBA8888
            else:
                qformat = QtGui.QImage.Format_RGB888

        outImage = QtGui.QImage(
            img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.lbl_cam.setPixmap(QtGui.QPixmap.fromImage(outImage))
            self.lbl_cam.setScaledContents(True)

    def snap(self):
        try:
            self.x1, self.y1, self.x2, self.y2 = 20, 20, 220, 270
            img_cropped = self.image[self.y1:self.y2, self.x1:self.x2]
                
            cv2.imwrite(jsd["path1"], img_cropped)
            
            self.lbl_img_snap.setPixmap(QtGui.QPixmap(jsd["path1"]))
            self.lbl_img_snap.show()

            edges = cv2.Canny(img_cropped, 75, 150)
            cv2.imwrite(jsd["path2"], edges)

            user_id = self.info['id']
            log_type = jsd["lg_log"]
            log_data = "User: "+self.info['id']+" snaped successfully"
            action = "Snap"
            risk = jsd["rsk_none"]

            utility.write_log(user_id, log_type, log_data, action, risk)

        except:

            QtWidgets.QMessageBox.critical(
                self, 'Error', "Error Taking Snap. Please Try Again Later!!!")
            user_id = jsd["system"]
            log_type = jsd["lg_error"]
            log_data = "Snapping failed for user: "+self.info['id']
            action = "Snap"
            risk = jsd["rsk_high"]

            utility.write_log(user_id, log_type, log_data, action, risk)

        try:

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
                3: '4',
                4: '5',
                5: '6',
                6: '7',
                7: '8',
                8: '9',
                9: 'A',
                10: 'B',
                11: 'C',
                12: 'D',
                13: 'E',
                14: 'F',
                15: 'G',
                16: 'H',
                17: 'I',
                18: 'K',
                19: 'L',
                20: 'M',
                21: 'N',
                22: 'O',
                23: 'P',
                24: 'Q',
                25: 'R',
                26: 'S',
                27: 'T',
                28: 'U',
                29: 'V',
                30: 'W',
                31: 'X',
                32: 'Y',

            }

            _dir = jsd["path2"]

            # input
            model = Sequential()
            model.add(Conv2D(32, (3, 3), input_shape=input_shape, padding='same'))
            model.add(Dropout(0.2))
            #model.add(MaxPooling2D(pool_size=(2, 2)))

            # first convo
            model.add(Conv2D(32, (3, 3), padding='valid'))
            model.add(Activation('relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Dropout(0.2))

            # second convo
            model.add(Conv2D(64, (3, 3), padding='valid'))
            model.add(Activation('relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Dropout(0.2))

            # third convo
            model.add(Conv2D(64, (3, 3), padding='valid'))
            model.add(Activation('relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Dropout(0.2))

            # fourth convo
            model.add(Conv2D(128, (3, 3), padding='valid'))
            model.add(Activation('relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Dropout(0.2))

            # fifth convo
            model.add(Conv2D(128, (3, 3), padding='valid'))
            model.add(Activation('relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Dropout(0.2))

            # fully connected
            model.add(Flatten())
            model.add(Dense(256))
            model.add(Activation('relu'))
            model.add(Dropout(0.5))
            model.add(Dense(33))
            model.add(Activation('softmax'))

            # load model
            model.load_weights('./models/trained_model.h5')

            model.compile(loss='categorical_crossentropy',
                            optimizer=Adam(lr=1e-3),
                            metrics=['categorical_accuracy'])

            img = image.load_img(_dir, target_size=(img_width, img_height))

            x = image.img_to_array(img)

            x = np.expand_dims(x, axis=0)

            images = np.vstack([x])

            p_classes = model.predict_classes(images)
            
            letter = names[p_classes[0]]
            print(letter)
            self.lbl_ans.setText(letter)

            # End Of CNN Predictor Code Block

            user_id = self.info['id']
            log_type = jsd["lg_log"]
            log_data = "User: " + \
                self.info['id']+" predicted the letter or number: " + \
                letter + " successfully"
            action = "Prediction"
            risk = jsd["rsk_none"]

            utility.write_log(user_id, log_type, log_data, action, risk)

        except:

            QtWidgets.QMessageBox.critical(
                self, 'Error', "Error In Prediction. Please Try Again Later!!!")
            user_id = jsd["system"]
            log_type = jsd["lg_error"]
            log_data = "Prediction failed for user: "+self.info['id']
            action = "Prediction"
            risk = jsd["rsk_high"]

            utility.write_log(user_id, log_type, log_data, action, risk)

    def back(self):
        self.mn = main()
        self.mn.show()
        self.close()

        user_id = self.info['id']
        log_type = jsd["lg_log"]
        log_data = "User: "+self.info['id']+" left predictor"
        action = "Predictor"
        risk = jsd["rsk_none"]

        utility.write_log(user_id, log_type, log_data, action, risk)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # lg = login()
    # lg.show()
    ld = loading()
    ld.show()
    sys.exit(app.exec_())
