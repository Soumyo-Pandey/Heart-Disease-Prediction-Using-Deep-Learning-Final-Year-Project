import os
import cv2
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


classifier = linear_model.LogisticRegression(max_iter=1000)

# Non-Binary Image Classification using Convolution Neural Networks
'''
path = 'DatasetImages'

labels = []
X_train = []
Y_train = []

normal_start = 0
abnormal_start = 0
dataset = pd.read_csv('heart.csv')
dataset = dataset.values
cols = dataset.shape[1] - 1
X = dataset[:,0:cols]
Y = dataset[:,cols]
X = normalize(X)
heart_normal = []
heart_abnormal = []
for i in range(len(Y)):
    if Y[i] == 0:
        heart_normal.append(X[i])
    if Y[i] == 1:
        heart_abnormal.append(X[i])
heart_normal = np.asarray(heart_normal)      
heart_abnormal = np.asarray(heart_abnormal)
print(heart_normal)
print(heart_abnormal)
print(X.shape)
print(heart_normal.shape) 
print(heart_abnormal.shape)

def merge(img,heart):
    temp = []
    for i in range(len(img)):
        temp.append(img[i])
    for i in range(len(heart)):
        temp.append(heart[i])
    temp = np.asarray(temp)
    return temp.astype(np.float32)
for root, dirs, directory in os.walk(path):
    for j in range(len(directory)):
        name = os.path.basename(root)
        print(name+" "+root+"/"+directory[j]+" "+str(np.asarray(X_train).shape))
        if 'Thumbs.db' not in directory[j]:
            img = cv2.imread(root+"/"+directory[j],0)
            img = cv2.resize(img, (32,32))
            im2arr = np.array(img)
            if name == 'normal':
                Y_train.append(0)
                if normal_start < len(heart_normal):
                    data = merge(im2arr.ravel(),heart_normal[normal_start])
                    X_train.append(data)
                else:
                    normal_start = 0
                    data = merge(im2arr.ravel(),heart_normal[normal_start])
                    X_train.append(data)
                normal_start = normal_start + 1
            if name == 'abnormal':
                Y_train.append(1)
                if abnormal_start < len(heart_abnormal):
                    data = merge(im2arr.ravel(),heart_abnormal[abnormal_start])
                    X_train.append(data)
                else:
                    abnormal_start = 0
                    data = merge(im2arr.ravel(),heart_abnormal[abnormal_start])
                    X_train.append(data)
                abnormal_start = abnormal_start + 1
        
X_train = np.asarray(X_train)
Y_train = np.asarray(Y_train)
indices = np.arange(X_train.shape[0])
np.random.shuffle(indices)
X_train = X_train[indices]
Y_train = Y_train[indices]
Y_train = to_categorical(Y_train)
print(X_train.shape)
np.save('model/X.txt',X_train)
np.save('model/Y.txt',Y_train)
print(Y_train)

#X_train = X_train.astype('float32')
#X_train = X_train/255
'''
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


'''
y = np.argmax(Y, axis=1)
print(y)
#calculate swarm particle
def f_per_particle(m, alpha):
    total_features = 1037
    if np.count_nonzero(m) == 0:
        X_subset = X_train
    else:
        X_subset = X_train[:,m==1]
    classifier.fit(X_subset, y)
    P = (classifier.predict(X_subset) == y).mean()
    j = (alpha * (1.0 - P) + (1.0 - alpha) * (1 - (X_subset.shape[1] / total_features)))
    return j

def f(x, alpha=0.88):
    n_particles = x.shape[0]
    j = [f_per_particle(x[i], alpha) for i in range(n_particles)]
    return np.array(j)

options = {'c1': 0.5, 'c2': 0.5, 'w':0.9, 'k': 5, 'p':2}
dimensions = 1037 # dimensions should be the number of features
optimizer = ps.discrete.BinaryPSO(n_particles=5, dimensions=dimensions, options=options)
cost, pos = optimizer.optimize(f, iters=2)
X_selected_features = X_train[:,pos==1]  # subset    
print(X_selected_features.shape)
print(X_selected_features)
X = np.load('model/X.txt.npy')
X = X[:,pos==1]
print(X.shape)
'''
'''
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
print(X_train.shape)
cnn_model = Sequential()
cnn_model.add(Dense(512, input_shape=(X_train.shape[1],)))
cnn_model.add(Activation('relu'))
cnn_model.add(Dropout(0.3))
cnn_model.add(Dense(512))
cnn_model.add(Activation('relu'))
cnn_model.add(Dropout(0.3))
cnn_model.add(Dense(2))
cnn_model.add(Activation('softmax'))
cnn_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
acc_history = cnn_model.fit(X, Y, epochs=50, validation_data=(X_test, y_test))
'''
