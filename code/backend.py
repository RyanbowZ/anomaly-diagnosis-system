import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from scipy.io import loadmat
from sklearn.externals import joblib
import time
import json
from flask_cors import CORS
from flask import Flask, request, jsonify,make_response  # 导入Flask类
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from sklearn.svm import LinearSVC
app = Flask(__name__)  # 实例化flask
CORS(app)
@app.route('/ainfo', methods=['GET', 'POST'])

def testGet():
    data=request.get_json(silent=True)

    fileContenttrain=data["fileContent1"]
    fileContenttest=data["fileContent2"]
    #arith=data["arithmetic"]
    varNumber=data["varNumber"]
    judgestate=data["state"]
    print(judgestate)
   # print(arith)
    print(varNumber)

    train_y=[]
    train_x=[]

    if judgestate==1:
        arith=data["arithmetic"]
        for i in range(1,int(varNumber)):
            filetrain = pd.read_csv( fileContenttrain + r"/d"+str('%02d'%i)+".dat", sep = '/t', header=None, engine='python')
            #filetrain = loadmat( fileContenttrain + r"\d"+str('%02d'%i)+".dat", sep = '/t', header=None, engine='python')
            df = filetrain.iloc[:,0].str.split('  ',expand=True).astype('float')
            train_list = np.array(df)
            num = train_list.shape[0]#行数

            file_index=i
            start_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            interval='5S'
            te_input = pd.DataFrame(data=list(zip(pd.date_range(start=start_time,periods=num,freq=interval),train_list,np.full(num,int(file_index)))),columns=['time_create','train_x','label'])

            for x in range(len(te_input['train_x'])):
                train_x.append(list(te_input['train_x'][x]))
                train_y.append(i)
            if len(te_input['train_x'])*int(varNumber)>=10000:
                return json.dumps({"recommend":1})
                #智能匹配神经网络算法训练
        if arith=='Random Forest':
            clf=RandomForestClassifier(n_estimators=200)
            clf.fit(train_x,train_y)
        elif arith=='PCA':
            pca = PCA(n_components=50,svd_solver='randomized',whiten=True).fit(train_x)#??????????
            X_trian_pca = pca.transform(train_x)
            #clf = pca.fit(X_trian_pca,train_y)
            clf = LinearSVC().fit(X_trian_pca,train_y)
        elif arith=='SVM':
            clf = GaussianNB()
            clf.fit(train_x, train_y)
        elif arith=='BPN':
            clf=KNeighborsClassifier()
            clf.fit(train_x,train_y)

        joblib.dump(clf,arith+"_model_full.m")
        print("Test Done!")
        sendjs={"data":0,"tr":1,"judge":0,"end":0}
        return json.dumps(sendjs)


    elif judgestate==2:
        arith=data["arithmetic"]
        rownum=data["num"]
        clf = joblib.load(arith+"_model_full.m") #调用
        rf = loadmat(fileContenttest + r"\TE_TEST_01.mat")

        test_x=rf['test']
        print(rownum)
        if rownum<(len(test_x)):
            sample = test_x[rownum,:].reshape(1,-1)
            if arith=='Random Forest':
                y_pre=clf.predict(sample)
            elif arith=='PCA':
                for i in range(1,int(varNumber)):
                    filetrain = pd.read_csv( fileContenttrain + r"/d"+str('%02d'%i)+".dat", sep = '/t', header=None, engine='python')
                    #filetrain = loadmat( fileContenttrain + r"\d"+str('%02d'%i)+".dat", sep = '/t', header=None, engine='python')
                    df = filetrain.iloc[:,0].str.split('  ',expand=True).astype('float')
                    train_list = np.array(df)
                    num = train_list.shape[0]#行数

                    file_index=i
                    start_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    interval='5S'
                    te_input = pd.DataFrame(data=list(zip(pd.date_range(start=start_time,periods=num,freq=interval),train_list,np.full(num,int(file_index)))),columns=['time_create','train_x','label'])

                    for x in range(len(te_input['train_x'])):
                        train_x.append(list(te_input['train_x'][x]))
                    #train_y.append(i)
                pca = PCA(n_components=50,svd_solver='randomized',whiten=True).fit(train_x)
                X_test_pca = pca.transform(sample)
                y_pre = clf.predict(X_test_pca)
            elif arith=='SVM':
                y_pre = clf.predict(sample)
            elif arith=='BPN':
                y_pre = clf.predict(sample)
            print(y_pre)
            samplist=sample[0].tolist()
            print(samplist)
            if rownum==(len(test_x)-1):
                sendjs={"data":samplist,"tr":0,"judge":y_pre.tolist(),"end":1}
            else:
                #sendjs={"data":samplist,"tr":0,"judge":y_pre.tolist(),"end":0}
                sendjs={"data":samplist,"tr":0,"judge":0,"end":0}
            return json.dumps(sendjs)

    elif judgestate==3:
        for i in range(1,int(varNumber)):
            filetrain = pd.read_csv( fileContenttrain + r"/d"+str('%02d'%i)+".dat", sep = '/t', header=None, engine='python')
            #filetrain = loadmat( fileContenttrain + r"\d"+str('%02d'%i)+".dat", sep = '/t', header=None, engine='python')
            df = filetrain.iloc[:,0].str.split('  ',expand=True).astype('float')
            train_list = np.array(df)
            num = train_list.shape[0]#行数

            file_index=i
            start_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            interval='5S'
            te_input = pd.DataFrame(data=list(zip(pd.date_range(start=start_time,periods=num,freq=interval),train_list,np.full(num,int(file_index)))),columns=['time_create','train_x','label'])

            if len(te_input['train_x'])*int(varNumber)>=10000:
                return json.dumps({"recommend":1})
            else:
                return json.dumps({"recommend":2})

    return "hello"
    # todo something




if __name__ == '__main__':

    app.run()




