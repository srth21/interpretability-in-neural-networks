# -*- coding: utf-8 -*-
"""Keras CNN for Tiny Image Net

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HOLTzw2snl8n_6qpJnqdYw_Q-WiMftWN
"""

from google.colab import drive
drive.mount("/content/gdrive")

#loading the dataset
#the data is a pickle file which stores a list
#the list has 2 elements : x and y

import pickle

x,y = pickle.load(open("/content/gdrive/My Drive/8th Semester Project/data.pickle","rb"))

#Checking if the number of samples is the same for both x and y

len(x)

len(y)

assert len(x) == len(y)

#importing libraries
#need sklearn to split the data into train and test

import sklearn
import numpy as np

import keras

#some images have only one channel 
#so need to convert them into 3
#use sklearn for this

from skimage.color import gray2rgb

for i in range(len(x)):
  if(x[i].shape !=(64,64,3)):
    x[i] = gray2rgb(x[i])

#checking if all images have three channels

error = 0

for i in range(len(x)):
  if(x[i].shape !=(64,64,3)):
    error+=1

error

#data augmentation

import random
import skimage as sk
from skimage import transform
from skimage import util

#Type 1 : Horizontal Flip

def horizontal_flip(image_array):
    # horizontal flip doesn't need skimage, it's easy as flipping the image array of pixels !
    return image_array[:, ::-1]

#Type 2 : Random Noise

def random_noise(image_array):
  return sk.util.random_noise(image_array)

#Type 3 : Random Rotation

def random_rotation(image_array):
    # pick a random degree of rotation between 25% on the left and 25% on the right
    random_degree = random.uniform(-25, 25)
    return sk.transform.rotate(image_array, random_degree)

#Transform Example

image = x[0]

image.shape

import matplotlib.pyplot as plt

plt.imshow(image)

y[0]

#Horizontal flip

image_flipped = horizontal_flip(image)

plt.imshow(image_flipped)

image_flipped.shape

#Random Noise

image_noise = random_noise(image)

plt.imshow(image_noise)

image_noise.shape

#Random Rotation

image_rotated = random_rotation(image)

plt.imshow(image_rotated)

image_rotated.shape

len(x)

from keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    featurewise_center=True,
    featurewise_std_normalization=True,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True)

for i in range(100000):
  img = x[i]
  op = y[i]
  img_r = datagen.random_transform(img)
  x.append(img_r)
  y.append(op)
  if(i%1000==0):
    print("Done for : ",i,"/100000")

len(x)

len(y)

for i in range(len(x)):
  if(x[i].shape !=(64,64,3)):
    error+=1

error

#Checking size of each class

size = {}

for i in range(len(x)):
  if(y[i] not in size):
    size[y[i]] = 1
  else:
    size[y[i]] += 1

set(size.values())

#converting y into one hot encoded vectors

y = keras.utils.to_categorical(y, num_classes=200, dtype='float32')

#pickle.dump([x,y],open("/content/gdrive/My Drive/8th Semester Project/data_1.pickle","wb"))

#Train and Test Split

import sklearn
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.15)

x_train = np.reshape(x_train,(-1,64,64,3))

x_test = np.reshape(x_test,(-1,64,64,3))

len(x_train)

#Checking an image

plt.imshow(x_train[0])

np.argmax(y_train[0])

assert len(x_train)==len(y_train) and len(x_test)==len(y_test)

x_train[0].shape

y_train[0]

#making the CNN Model

from keras.models import Sequential

from keras import regularizers

from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense, Dropout, Flatten

batch_size = 512
num_classes = 200
number_of_epochs = 100

model = Sequential()

model.add(Conv2D(32, (3, 3), input_shape=(64,64,3), padding='same',activation='relu'))
model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))

model.add(Flatten())

model.add(Dense(1024, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
model.add(Dropout(0.40))

model.add(Dense(512, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
model.add(Dropout(0.35))

model.add(Dense(200, activation='softmax' ))

model.compile(loss=keras.losses.categorical_crossentropy,optimizer=keras.optimizers.Adadelta(),metrics=['accuracy'])

model.summary()

np.array([1,2,3])

saver = keras.callbacks.ModelCheckpoint("/content/gdrive/My Drive/8th Semester Project/weights.{epoch:02d}-{val_loss:.2f}.hdf5", monitor='val_loss', verbose=0, save_best_only=False, save_weights_only=False, mode='auto', period=1)

early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=0, verbose=0, mode='auto', baseline=None, restore_best_weights=False)

model.fit(x_train, y_train,batch_size=batch_size,epochs=number_of_epochs,verbose=1,validation_data=(x_test, y_test))

model.save('/content/gdrive/My Drive/8th Semester Project/my_model_added_reg.h5')