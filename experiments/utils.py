import glob
import sys
import pickle
from aienvs.FactoryFloor.FactoryFloorState import encodeStateAsArray
import numpy as np

def preprocess(dirname, robotIdList):
    all_pickle_files = glob.glob( dirname + '/**/*.pickle', recursive=True )

    states = []
    actions = []

    for filename in all_pickle_files:
        print("Processing " + filename)
        with open (filename, 'rb') as instream:
            instream = open(filename, 'rb')
            while True:
                try:
                    data=pickle.load(instream)
                    for robotId in robotIdList:
                        actions.append(data.get("actions").get(robotId))
                        states.append(encodeStateAsArray(data.get("observation")))
                except EOFError:
                    break

    if len(states)!=len(actions):
        raise "Something went wrong"
    
    print("STATES AND ACTIONS PROCESSED: " + str(len(states)))
    print("MEMORY USED BY STATES AND ACTIONS: " + str(sys.getsizeof(states)) + str(sys.getsizeof(actions)) )

    return np.array(states), np.array(actions)


import keras
from keras.models import Sequential, load_model
from keras.layers import Flatten, Dense, Conv2D, MaxPooling2D, Cropping2D, Dropout, Convolution2D, Activation, Lambda
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import plot_model

#need to change def. arg manually for evaluation
def classification_model(shape=(4,4,4)):
    model = Sequential()
    model.add(Convolution2D(16,(2,2), input_shape=shape, activation='relu'))
    model.add(Convolution2D(32,(2,2), activation='relu'))
 #   model.add(Convolution2D(4,(2,2), activation='relu'))
   # model.add(Dropout(0.5))
   # model.add(Flatten())
    model.add(Flatten())
  #  model.add(Dense(192, activation='relu'))
 #   model.add(Dense(128, input_dim=1, activation='relu'))
  #  model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(5, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    plot_model(model, to_file='model.png', show_shapes=True)

    return model



