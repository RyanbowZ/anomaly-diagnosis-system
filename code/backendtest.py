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
import re
'''rf = loadmat(filepath)
    train_x=rf['train_x']
    train_y=rf['train_y'].ravel()
    test_x=rf['test_x']
    expected=rf['expected'].ravel()
    print("filecont:"+data["fileContent"])
    print("arithmetic:"+data["arithmetic"])
    print("varNumber:"+data["varNumber"])
    print("interval:"+data["interval"])'''
'''x=1
a=str('%02d'%x)
#print(a)
file = pd.read_csv( r"D:\Documents\大创\训练集" + r"\d"+str('%02d'%x)+".dat", sep = '/t', header=None, engine='python')'''
        #训练
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
clf=RandomForestClassifier(n_estimators=800,max_features=8)
y=[]
train_x=[]
test_x=[]
#print(re.split("   ",file[0][0]))

for i in range(1,22):
    filetrain = pd.read_csv( r"D:\Documents\大创\训练集" + r"\d"+str('%02d'%i)+".dat", sep = '/t', header=None, engine='python')
        #训练

    #clf=RandomForestClassifier(n_estimators=800,max_features=8)
    df = filetrain.iloc[:,0].str.split('  ',expand=True).astype('float')
    train_list = np.array(df)
    num = train_list.shape[0]#行数

    file_index=i
    start_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    interval='5S'
    te_input = pd.DataFrame(data=list(zip(pd.date_range(start=start_time,periods=num,freq=interval),train_list,np.full(num,int(file_index)))),columns=['time_create','train_x','label'])
    #print(te_input['train_x'])
    #print(len(te_input['train_x']))
    for x in range(len(te_input['train_x'])):
        train_x.append(list(te_input['train_x'][x]))
        #print(list(te_input['train_x'][x]))
        y.append(i)
    #print(len(train_x))
    #print(train_x)
    #y=[i for x in range(len(te_input['train_x']))]
    #clf.fit(te_input['train_x'][0].reshape(-1, 1),y)
#print(len(train_x),len(y))
clf.fit(train_x,y)
joblib.dump(clf,"train_new_model_full.m")

#------------------------------------------
''''for j in range(len(filetrain)):
    y=[]
    for j in range(len(filetrain)):
        y=[]
        train_x=filetrain[0][j].split()

        for var in train_x:
            var=float(var)
        #trainsamp[j]=train_x
        #train_x=np.array(train_x).reshape(-1,1)
        train_x=np.array(train_x).reshape(-1,1)
        for x in range(len(train_x)):
            y.append(i)
        print(train_x)
        clf.fit(train_x,y)
        filetrain[0][j]=filetrain[0][j].split()'''''
    #y.append(i)
    #y=np.array(y)
    #trainsamp=np.array(filetrain[0]).reshape(-1,1)
    #trainsamp=np.concatenate(trainsamp, axis=0)
    #print(filetrain[0])
    #print(len(y))
''''weidian=[[0 for i in range(len(filetrain[0][1]))]for n in range(len(filetrain))]
    print(weidian)
    for j in range(len(filetrain)):
        for x in range(len(filetrain[0][j])):

            weidian[x].append(filetrain[0][j][x])

    print(weidian)'''''
    #trainsamp=np.concatenate(filetrain[0], axis=0).reshape(-1,1)
    #print(trainsamp)
    #clf.fit(trainsamp,y)

#joblib.dump(clf, "newtrain_model.m") #存储
#--------------------
''''
clf = joblib.load("train_new_model.m") #调用
for i in range(1,2):
    filetest = pd.read_csv( r"D:\Documents\大创\测试集" + r"\d"+str('%02d'%i)+"_te.dat", sep = '/t', header=None, engine='python')
    df = filetest.iloc[:,0].str.split('  ',expand=True).astype('float')
    test_x =np.array(df)
    num = test_x.shape[0]#行数

    file_index=i
    start_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    interval='5S'
    te_input = pd.DataFrame(data=list(zip(pd.date_range(start=start_time,periods=num,freq=interval),test_x)),columns=['time_create','test_x'])
    #print(te_input['train_x'])
    sample=[]
    sample.append(list(te_input['test_x'][0]))
    #print(sample)
    print(clf.predict(sample))

    #------------------------
    #for x in range(len(te_input['test_x'])):
        #test_x.append(list(te_input['test_x'][x]))
        #print(te_input['test_x'][x])
        #print(clf.predict(te_input['test_x'][x]))
for j in range(len(filetest)):
        test_x=re.split("   ",filetest[0][j])
        y_hat=str(clf.predict(test_x))
        print(y_hat)'''''
    #sample = test_x[i,:].reshape(1,-1)#这里可改'''




#@app.route('/', methods=['GET', 'DELETE', 'POST'])





#导入文件
'''filepath='D:/Documents/大创/ddata00.mat'
rf = loadmat(filepath)
train_x=rf['train_x']
train_y=rf['train_y'].ravel()
test_x=rf['test_x']
expected=rf['expected'].ravel()'''

#训练
'''clf=RandomForestClassifier(n_estimators=800,max_features=8)
clf.fit(train_x,train_y)


joblib.dump(clf, "train_model.m") #存储
#===========
# clf = joblib.load("train_model.m") #调用
#
# #预测
# sample = test_x[0,:].reshape(1,-1)#这里可改
# y_hat=clf.predict(sample)
# print(y_hat)
    #预测
    for i in range(1000):
        sample = test_x[i,:].reshape(1,-1)#这里可改
        y_hat=str(clf.predict(sample))
        #print(sample[0])
        sendlist=[]
        sendlist.append(int(y_hat[1:-1]))
        sendlist=sendlist+list(sample[0])
        #print(sendlist)
        json_str = json.dumps(sendlist)'''

