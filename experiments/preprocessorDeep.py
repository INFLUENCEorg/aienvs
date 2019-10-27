from keras.wrappers.scikit_learn import KerasClassifier
from utils import preprocess, classification_model
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import np_utils
import os
import sys
import numpy as np
import configargparse

def main():
    parser = configargparse.ArgParser()
    parser.add('-c', '--my-config', is_config_file=True, help='config file path')
    parser.add('-d', '--dirname', dest="dirname")
    parser.add('-o', '--outputdir', dest="outputdir")
    parser.add('-r', '--robotIds', dest="robotIds", action="append")
    parser.add('-e', '--evaluate', dest="evaluate", action="store_true", default=False)
    parser.add('-b', '--batchSize', dest="batchSize", type=int)
    parser.add('-p', '--epochs', dest="epochs", type=int)

    argums = parser.parse_args()

    datagen = ImageDataGenerator(
        featurewise_center=False,
        featurewise_std_normalization=False,
        rotation_range=0,
        width_shift_range=0.0,
        height_shift_range=0.0,
        horizontal_flip=False)
    
    for robotId in argums.robotIds:
        X_train, y_train = preprocess(argums.dirname, [robotId])
        print(np.histogram(y_train))

        print(X_train.shape)
        print(y_train.shape)

        dummy_y = np_utils.to_categorical(y_train, num_classes=5)
        
        if(argums.evaluate):
            estimator = KerasClassifier(classification_model, epochs=argums.epochs, batch_size=argums.batchSize, verbose=True)
            kfold = KFold(n_splits=5, shuffle=True)
            results = cross_val_score(estimator, X_train, dummy_y, cv=kfold)
            print("Accuracy, stdev %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))	
        else:
            os.makedirs(argums.outputdir, exist_ok=True)
            generator = datagen.flow(X_train, dummy_y, batch_size=argums.batchSize)
            model=classification_model(X_train.shape[1:4])
            model.fit_generator(generator, steps_per_epoch=len(X_train) / argums.batchSize, nb_epoch=argums.epochs)
            output_file = argums.outputdir + "/" + robotId + ".h5"
            model.save(output_file)

if __name__ == "__main__":
        main()
	
