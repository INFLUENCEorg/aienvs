import glob
import sys
import pickle
from aienvs.FactoryFloor.FactoryFloorState import encodeStateAsArray
import numpy as np

def preprocess(dirname, width, height, robotIdList):
    all_pickle_files = glob.glob( dirname + '**/*.pickle', recursive=True )

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
                        states.append(encodeStateAsArray(data.get("observation"), width, height, robotId))
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
from keras.utils import np_utils
from keras.utils import plot_model
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from keras.preprocessing.image import ImageDataGenerator
from aienvs.utils import getParameters

def classification_model():
    model = Sequential()
   # model.add(Convolution2D(16,(2,2), input_shape=(5,4,3), activation='relu'))
   # model.add(Dropout(0.5))
   # model.add(Flatten())
    model.add(Flatten(input_shape=(5,4,3)))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.7))
    model.add(Dense(192, activation='relu'))
    model.add(Dropout(0.7))
 #   model.add(Dense(128, input_dim=1, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.7))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.7))
    model.add(Dense(16, activation='relu'))
    model.add(Dropout(0.7))
    model.add(Dense(5, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    plot_model(model, to_file='model.png', show_shapes=True)

    return model



def main():
    if(len(sys.argv) == 2):
        param_filename = str(sys.argv[1])
        parametersDict = getParameters(param_filename)
        dirname = parametersDict["data"]
        width = parametersDict["width"]
        height = parametersDict["height"]
        robotIds = parametersDict["robotIds"]
        evaluate = parametersDict["evaluate"]
        output_file = parametersDict["output_file"]
    elif(len(sys.argv) == 7):
        dirname = str(sys.argv[1])
        width = int(sys.argv[2])
        height = int(sys.argv[3])
        robotIds = str(sys.argv[4]).split(",")
        evaluate = bool(int(sys.argv[5]))
        output_file = str(sys.argv[6])
    else:
        raise "Either 1 or 6 arguments"

    X_train, y_train = preprocess(dirname, width, height, robotIds)
    print(np.histogram(y_train))
    import pdb
    pdb.set_trace()
    breakpoint()

    datagen = ImageDataGenerator(
        featurewise_center=False,
        featurewise_std_normalization=False,
        rotation_range=0,
        width_shift_range=0.0,
        height_shift_range=0.0,
        horizontal_flip=False)

    print(X_train.shape)
    print(y_train.shape)

    dummy_y = np_utils.to_categorical(y_train)
    
    batch_size=600
    epochs=100

    if(eval(evaluate)):
        estimator = KerasClassifier(classification_model, epochs=epochs, batch_size=batch_size, verbose=True)
        kfold = KFold(n_splits=5, shuffle=True)
        results = cross_val_score(estimator, X_train, dummy_y, cv=kfold)
        print("Accuracy, stdev %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))	
        # for predicting dummy_y from y_train
 #       estimator.fit(y_train, dummy_y, epochs=epochs, batch_size=batch_size, verbose=True)
 #       print(estimator.predict_proba([1]))
 #       print(estimator.predict_proba([2]))
 #       print(estimator.predict_proba([0]))
    else:
        generator = datagen.flow(X_train, dummy_y, batch_size=batch_size)
        model=classification_model()
        model.fit_generator(generator, steps_per_epoch=len(X_train) / batch_size, nb_epoch=epochs)
     #   model.fit(X_train, dummy_y, epochs=epochs, batch_size=batch_size, verbose=True)
        model.save(output_file)

    #model = load_model("robot1.h5")
    #image = X_train[0,:,:,:]
    #image_aug = np.expand_dims(image, axis=0)
    #prediction = model.predict(image_aug, batch_size=1)

if __name__ == "__main__":
        main()
	
