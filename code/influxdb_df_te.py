#influxdb test based on Dataframe

import argparse
import pandas as pd
import numpy as np
from influxdb import DataFrameClient
#import socket
import time
import threading
import sys
import cgi
import cgitb
import json
import cgi
import traceback
import cgitb
import json
import sys
from flask_cors import CORS
from flask import Flask, request, jsonify,make_response  # 导入Flask类

from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

app = Flask(__name__)  # 实例化flask
CORS(app)

@app.route('/ainfo', methods=['GET', 'POST'])
def testGet():
    data=request.get_json(silent=True)

    return "hello"

filepath = "D:/Documents/大创/TE_process/"
te = pd.DataFrame(columns=['sample index','x','label'])#data of testing
pd.set_option('display.width', None)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行

''''class Client:
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
        while True:
            self.client.send(mes.encode())
            time.sleep(1)  # 如果想验证长时间没发数据，SOCKET连接会不会断开，则可以设置时间长一点

    def resv(self):
        while True:
            data = self.client.recv(self.BUF_SIZE)
            text = data.decode()
            print(text)

    def startResv(self):
        t = threading.Thread(target=self.resv)
        t.start()

    def close(self):
        self.client.close()'''''

def te_input(filepath,file_index,start_time,interval):
    file = pd.read_csv(filepath + "d%s_te.dat"%file_index, sep = '/t', header=None, engine='python')
    df = file.iloc[:,0].str.split('  ',expand=True).astype('float')
    test_x = np.array(df.iloc[:100,:])
    num = test_x.shape[0]#行数
    te_input = pd.DataFrame(data=list(zip(range(1+(int(file_index)-1)*num,num+1+(int(file_index)-1)*num),test_x,np.full(num,int(file_index)))),
                                index=pd.date_range(start=start_time,
                                                    periods=num,freq=interval),columns=['sample_index','x','label'])
    return te_input



def main(dbname,measurements,tags,dataset,query,host='localhost', port=8086):
    user = 'root'
    password = 'root'
    protocol = 'line'#行协议

    client = DataFrameClient(host, port, user, password, dbname)
    print("创建数据库: " + dbname)
    listdb=client.get_list_database()
    dbn = [item[key] for item in listdb for key in item]
    if dbname in dbn:
        client.drop_database(dbname)
    client.create_database(dbname)
    fo = open("D:/Documents/大创/new_result2.txt", "w")
    for i in range(dataset.shape[0]-1):
        fo.write(str(dataset.iloc[i:i+1]))
        client.write_points(dataset.iloc[i:i+1], measurements,{'Classes':tags},protocol=protocol)
        #time.sleep(0.2)
    fo.close()

    if query == False:
        pass
    elif query == True:
        result=client.query('select * from Tenessee_Eastman')#-------------------这里还需要进一步变通一下 满足不同的查询命令
                                                    #select * from Tenessee where class='training' #获取训练集
        #print(result)
        re=sorted(result.items())
        print('Measurement:'+re[0][0])
        print(re[0][1])
        fo = open("D:/Documents/大创/new_result.txt", "w")
        fo.write(str(result))
        fo.close()

        np.save('D:/Documents/大创/zyl_data.npy',result)
    else:
        print("parameter 'query' is not valid")

def parse_args():
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    app.run()
    np.set_printoptions(threshold=sys.maxsize)
    args = parse_args()
    filepath = "D:/Documents/大创/TE_process/"
    index=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21']
    index_small = ['01']
    for i in index_small:
        te=te_input(filepath,i,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'5S')
        main(dbname='industrial_database_te',measurements='Tenessee_Eastman',dataset=te,tags='testing',query=True,host=args.host, port=args.port)
    #client = Client("localhost",8083)
    #client.connect()
    #client.send('text')
