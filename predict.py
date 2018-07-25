from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from keras.optimizers import Adam
import tensorflow as tf
import keras
import sys
import os

from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import glob
import cv2
import logging

import requests
import json
import utility
import pickledb


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

logging.basicConfig(filename='Log/predict_log.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')
try:

    # dimensions of our images
    img_width, img_height = 200, 250

    if K.image_data_format() == 'channels_first':
        input_shape = (3, img_width, img_height)
    else:
        input_shape = (img_width, img_height, 3)

    try:
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

    

        _dir =  sys.argv[1]


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
        model.add(Dense(33))
        model.add(Activation('softmax'))

    

        #load model 
        model.load_weights('./models/trained_model_1.h5')

    except ValueError:
        logging.error('Class_Error: {}'.format('Invalid number of classes'))

    model.compile(loss='categorical_crossentropy',
                optimizer=Adam(lr=1e-3),
                metrics=['categorical_accuracy'])
    


    dir_files = glob.glob(_dir+'*.jpg')


    for _file in dir_files:
        file_path = _file
        

        # img = image.load_img(file_path, target_size=(img_width, img_height), grayscale=True)
        img = image.load_img(file_path, target_size=(img_width, img_height))
    
        x = image.img_to_array(img)

        x = np.expand_dims(x, axis=0)

        images = np.vstack([x])

        classes = model.predict(images)

        p_classes = model.predict_classes(images)
        # print (p_classes)
        letter = names[p_classes[0]]
        print (_file+" : "+letter)

except ValueError:
    logging.error('Input_Error: {}'.format('Invalid input found in the file'))
