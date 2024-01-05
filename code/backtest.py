import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from scipy.io import loadmat
from sklearn.externals import joblib
import time
import threading
import sys
import socket
import json
import cgi
import traceback
import cgitb
import json
import sys
from flask_cors import CORS
from flask import Flask, request, jsonify,make_response  # 导入Flask类
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
app = Flask(__name__)  # 实例化flask
CORS(app)


#def testGet():

arith='Random Forest'
if True:
       # rownum=data["num"]
    clf = joblib.load(arith+"_model_full.m") #调用
    rf = loadmat("D:/Documents/大创/data/test/TE_TEST_01.mat")

    test_x=rf['test']

    for i in range(len(test_x)):
        sample = test_x[i,:].reshape(1,-1)
        if arith=='Random Forest':
            y_pre=clf.predict(sample)
        elif arith=='PCA':
            pca = PCA(n_components=100,svd_solver='randomized',whiten=True).fit(train_x)
            X_test_pca = pca.transform(sample)
            y_pre = clf.predict(X_test_pca)
        elif arith=='SVM':
            y_pre = clf.predict(sample)
        else :#BPN
            y_pre = clf.predict(sample)
        print(y_pre)

        if i==(len(test_x)-1):
            sendjs={"data":sample,"tr":0,"judge":y_pre,"end":1}
        else:
            sendjs={"data":sample,"tr":0,"judge":y_pre,"end":0}








