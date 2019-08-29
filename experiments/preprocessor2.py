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
    else:
        raise "2 arguments needed"

    datagen = ImageDataGenerator(
        featurewise_center=False,
        featurewise_std_normalization=False,
        rotation_range=0,
        width_shift_range=0.0,
        height_shift_range=0.0,
        horizontal_flip=False)
    
    for robotId in robotIds:
        X_train, y_train = preprocess(dirname, width, height, [robotId])
        print(np.histogram(y_train))

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
        else:
            modeldir = dirname+"../models/"
            os.makedirs(modeldir, exist_ok=True)
            generator = datagen.flow(X_train, dummy_y, batch_size=batch_size)
            model=classification_model()
            model.fit_generator(generator, steps_per_epoch=len(X_train) / batch_size, nb_epoch=epochs)
            output_file = modeldir + robotId + ".h5"
            model.save(output_file)

if __name__ == "__main__":
        main()
	
