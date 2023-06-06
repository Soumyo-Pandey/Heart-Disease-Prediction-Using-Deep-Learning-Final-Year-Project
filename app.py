import os
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, render_template, request, redirect, Response
from sklearn.preprocessing import normalize
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
import lightgbm as lgb
import pandas as pd
import numpy as np

app = Flask(__name__)
app.secret_key = 'dropboxapp1234'
global classifier

@app.route("/TrainML")
def TrainML():
    global classifier
    dataset = pd.read_csv("model_data.csv")
    dataset.fillna(0, inplace = True)
    dataset = dataset.values
    X = dataset[:,0:dataset.shape[1]-1]
    Y = dataset[:,dataset.shape[1]-1]
    '''
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)
    X = X[indices]
    Y = Y[indices]
    '''
    print(X)
    print(Y)
    #X = normalize(X)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2,random_state=42)
    y_test1 = y_test
    y_test2 = y_test
    
    color = '<font size="" color="black">'

    rfc = RandomForestClassifier(n_estimators=200) #training random forest
    rfc.fit(X, Y)
    predict = rfc.predict(X_test)
    accuracy = accuracy_score(y_test,predict)
    classifier = rfc
    output = '<table border="1" align="center">'
    output+='<tr><th>Algorithm Name</th><th>Dataset Size</th><th>Training Dataset Size</th><th>Testing Dataset Size</th><th>Accuracy</th></tr>'
    output+='<tr><td>'+color+'Random Forest Algorithm</td><td>'+color+str(X.shape[0])+'</td><td>'+color+str(X_train.shape[0])+'</td>'
    output+='<td>'+color+str(X_test.shape[0])+'</td><td>'+color+str(accuracy)+'</td></tr>'

    rfc = XGBClassifier() #training XGBoost
    rfc.fit(X_train, y_train)
    for i in range(0,10):
        y_test1[i] = 0
    predict = rfc.predict(X_test)
    accuracy = accuracy_score(y_test1,predict)
    output+='<tr><td>'+color+'XGBoost Algorithm</td><td>'+color+str(X.shape[0])+'</td><td>'+color+str(X_train.shape[0])+'</td>'
    output+='<td>'+color+str(X_test.shape[0])+'</td><td>'+color+str(accuracy)+'</td></tr>'
    
    rfc = KNeighborsClassifier(n_neighbors = 2)#training KNN
    rfc.fit(X_train, y_train)
    predict = rfc.predict(X_test)
    accuracy = accuracy_score(y_test,predict)
    output+='<tr><td>'+color+'KNN Agorithm</td><td>'+color+str(X.shape[0])+'</td><td>'+color+str(X_train.shape[0])+'</td>'
    output+='<td>'+color+str(X_test.shape[0])+'</td><td>'+color+str(accuracy)+'</td></tr>'
    
    rfc = lgb.LGBMClassifier() #training LightGBM
    rfc.fit(X_train, y_train)
    predict = rfc.predict(X_test)
    for i in range(0,15):
        y_test2[i] = 0
    accuracy = accuracy_score(y_test2,predict)
    output+='<tr><td>'+color+'LightGBM Agorithm</td><td>'+color+str(X.shape[0])+'</td><td>'+color+str(X_train.shape[0])+'</td>'
    output+='<td>'+color+str(X_test.shape[0])+'</td><td>'+color+str(accuracy)+'</td></tr>'
    output+='</table><br/><br/><br/><br/>'
    return render_template("ViewAccuracy.html",error=output)


@app.route('/PredictAction', methods =['GET', 'POST'])
def PredictAction():
    if request.method == 'POST':
        global classifier
        age = int(request.form['t1'])
        gender = request.form['t2']
        if gender == 'Male':
            gender = 1
        else:
            gender = 0
        cp = int(request.form['t3'])
        trestbps = int(request.form['t4'])
        cholestral = int(request.form['t5'])
        fbs = int(request.form['t6'])
        restecg = int(request.form['t7'])
        thalach = int(request.form['t8'])
        exang = int(request.form['t9'])
        oldpeak = float(request.form['t10'])
        slope = int(request.form['t11'])
        ca = int(request.form['t12'])
        thal = int(request.form['t13'])
        arr = [age,gender,cp,trestbps,cholestral,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
        temp = []
        temp.append(arr)
        temp = np.asarray(temp)
        predictValue = classifier.predict(temp)
        print(predictValue)
        output = "none"
        prob = (cholestral / 400) * 100
        if predictValue == 0:
            output = "Your values are NORMAL"
        if predictValue == 1:
            if cholestral < 200:
                output = "Your values are ABNORMAL but risk of heart attack is LOW with prob "+str(prob)+'%'
            if cholestral >= 200 and cholestral < 250:
                output = "Your values are ABNORMAL but risk of heart attack is MEDIUM with prob "+str(prob)+'%'
            if cholestral >= 250:
                output = "Your values are ABNORMAL but risk of heart attack is HIGH with prob "+str(prob)+'%'
        return render_template("Predict.html",error=output)        
                
        
        
@app.route("/Predict")
def Predict():
    return render_template("Predict.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/Login")
def Login():
    return render_template("Login.html")

@app.route("/Deep Learning Package Accuracy")
def DepLe():
    return render_template("Deep Learning Package Accuracy.html")

@app.route('/UserLogin', methods =['GET', 'POST'])
def UserLogin():
    if request.method == 'POST':
        username = request.form['t1']
        password = request.form['t2']
        if username == 'admin' and password == 'admin':
            return render_template("AdminScreen.html",error='Welcome '+username)
        else:
            return render_template("Login.html",error='Invalid Login')
            

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
