from utils import preprocess, classification_model
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import np_utils
from aienvs.utils import getParameters
import os
import sys
import numpy as np


def main():
    if(len(sys.argv) == 3):
        param_filename = str(sys.argv[1])
        parametersDict = getParameters(param_filename)
        dirname = str(sys.argv[2])
        width = parametersDict["width"]
        height = parametersDict["height"]
        robotIds = parametersDict["robotIds"]
        evaluate = parametersDict["evaluate"]
        os.makedirs(dirname+"../models", exist_ok=True)
        output_file = dirname+"../models/robot.h5"
    elif(len(sys.argv) == 7):
        dirname = str(sys.argv[1])
        width = int(sys.argv[2])
        height = int(sys.argv[3])
        robotIds = str(sys.argv[4]).split(",")
        evaluate = bool(int(sys.argv[5]))
        output_file = str(sys.argv[6])
    else:
        raise "Either 2 or 6 arguments"

    X_train, y_train = preprocess(dirname, width, height, robotIds)
    print(np.histogram(y_train))

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
        #import pdb
        #pdb.set_trace()
        #incorrects = np.nonzero(estimator.predict_class(X_train).reshape((-1,)) != y_train)
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
	
