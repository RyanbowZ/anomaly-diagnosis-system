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

class Client:
    def __init__(self,host,port):
        self.port = port
        self.host = host
        self.status = 0
        self.BUF_SIZE = 1024

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳
        self.client.connect((self.host, self.port))

    def send(self,mes):
        client.startResv()
        #while True:
        self.client.send(mes.encode())
        time.sleep(0.5)  # 如果想验证长时间没发数据，SOCKET连接会不会断开，则可以设置时间长一点

    def resv(self):
        while True:
            data = self.client.recv(self.BUF_SIZE)
            text = data.decode()
            print(text)

    def startResv(self):
        t = threading.Thread(target=self.resv)
        t.start()

    def close(self):
        self.client.close()

#导入文件
filepath='D:/Documents/大创/ddata00.mat'
rf = loadmat(filepath)
train_x=rf['train_x']
#print((train_x))
train_y=rf['train_y'].ravel()
test_x=rf['test_x']
#print(len(train_y))
expected=rf['expected'].ravel()

''''#训练
clf=RandomForestClassifier(n_estimators=800,max_features=8)
clf.fit(train_x,train_y)


joblib.dump(clf, "train_model.m")'''
#===========
# clf = joblib.load("train_model.m") #调用
#
# #预测
# sample = test_x[0,:].reshape(1,-1)#这里可改
# y_hat=clf.predict(sample)
# print(y_hat)
if __name__ == '__main__':
    clf = joblib.load("train_model_new.m") #调用
    #client = Client("localhost",8084)
    #client.connect()
    #预测
    print(test_x[2,:].reshape(1,-1))
    for i in range(1000):
        sample = test_x[i,:].reshape(1,-1)#这里可改
        #print(sample)
        #y_hat=str(clf.predict(sample))
        #print(y_hat)
        #sendlist=[]
        #sendlist.append(int(y_hat[1:-1]))
        #sendlist=sendlist+list(sample[0])
        #print(sendlist)
        #json_str = json.dumps(sendlist)
        #client.send(json_str)'''''
