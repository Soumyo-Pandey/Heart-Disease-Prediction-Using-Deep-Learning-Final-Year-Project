import numpy as np
from genetic_selection import GeneticSelectionCV
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model

import numpy as np
from keras.utils.np_utils import to_categorical
from keras.layers import  MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D
from keras.models import Sequential
from keras.models import model_from_json
#import pickle
import pandas as pd
from sklearn.preprocessing import normalize
import pyswarms as ps
from SwarmPackagePy import testFunctions as tf
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from genetic_selection import GeneticSelectionCV
from sklearn.ensemble import RandomForestClassifier

def runAlg():
    X_train = np.load('model/X.txt.npy')
    Y = np.load('model/Y.txt.npy')  
    print(X_train.shape)
    y = np.argmax(Y, axis=1)
    estimator = linear_model.LogisticRegression(solver="liblinear", multi_class="ovr")
    selector = GeneticSelectionCV(estimator,
                                  cv=5,
                                  verbose=1,
                                  scoring="accuracy",
                                  max_features=5,
                                  n_population=50,
                                  crossover_proba=0.5,
                                  mutation_proba=0.2,
                                  n_generations=40,
                                  crossover_independent_proba=0.5,
                                  mutation_independent_proba=0.05,
                                  tournament_size=3,
                                  n_gen_no_change=10,
                                  caching=True,
                                  n_jobs=-1)
    selector = selector.fit(X_train, y)
    print(selector.support_)
    X_selected_features = X_train[:,selector.support_==True]
    X = np.load('model/X.txt.npy')
    X = X_train[:,selector.support_==True]
    print(X.shape)
    X = normalize(X)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
    print(X_train.shape)
    model = Sequential()
    model.add(Dense(30, input_dim=X_train.shape[1], activation='tanh'))
    model.add(Dense(20, activation='tanh'))
    model.add(Dense(2, activation='sigmoid'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    acc_history = model.fit(X, Y, epochs=50, validation_data=(X_test, y_test))

if __name__ == "__main__":
    runAlg()
