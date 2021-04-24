import base64
import numpy as np
import cv2

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, MaxPool2D

def stringToRGB(base64_string):
    imgdata = base64.b64decode(str(base64_string))
    im_arr = np.frombuffer(imgdata, dtype=np.uint8) 
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img


def get_model():
  model = Sequential()
  model.add(Conv2D(16, kernel_size = (3,3), input_shape = (28, 28, 3), activation = 'relu', padding = 'same'))
  model.add(Conv2D(32, kernel_size = (3,3), activation = 'relu'))
  model.add(MaxPool2D(pool_size = (2,2)))
  model.add(Conv2D(32, kernel_size = (3,3), activation = 'relu', padding = 'same'))
  model.add(Conv2D(64, kernel_size = (3,3), activation = 'relu'))
  model.add(MaxPool2D(pool_size = (2,2), padding = 'same'))
  model.add(Flatten())
  model.add(Dense(64, activation='relu'))
  model.add(Dense(32, activation='relu'))
  model.add(Dense(7, activation='softmax'))
  return model

