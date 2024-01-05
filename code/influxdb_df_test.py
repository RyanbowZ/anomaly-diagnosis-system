#influxdb test based on Dataframe

import argparse
import pandas as pd
import numpy as np
import datetime
from abc import abstractmethod
from sklearn.ensemble import RandomForestClassifier
from scipy.io import loadmat
from influxdb import DataFrameClient
import time


#load trainingset method

filepath = "D:/Documents/大创/TE_process/"
#tr = pd.DataFrame(columns=['sample_index','x','label'])#data of training
te = pd.DataFrame(columns=['sample index','x','label'])#data of testing

rowcount=0

'''def tr_input(filepath,file_index,start_time,interval):
    file = pd.read_csv(filepath + "d%s.dat"%file_index, sep = '/t', header=None, engine='python')
    df = file.iloc[:,0].str.split('  ',expand=True).astype('float')
    train_x = np.array(df)
    #train_x = np.array(df.iloc[:1,:1])#这里只是截取了一点数据
    num = train_x.shape[0]
    tr_input = pd.DataFrame(data=list(zip(range(1+(int(file_index)-1)*num,num+1+(int(file_index)-1)*num),train_x,np.full(num,int(file_index)))),
                            index=pd.date_range(start=start_time,
                                                periods=num,freq=interval),columns=['sample_index','x','label'])
    return tr_input'''

#load testingset method2
def te_input(filepath,file_index,start_time,interval):
    file = pd.read_csv(filepath + "d%s_te.dat"%file_index, sep = '/t', header=None, engine='python')
    df = file.iloc[:,0].str.split('  ',expand=True).astype('float')
    test_x = np.array(df.iloc[:20,:])
    #print(test_x)
    #test_x = np.array(df.iloc[:1,:1])
    num = test_x.shape[0]#行数
    te_input = pd.DataFrame(data=list(zip(range(1+(int(file_index)-1)*num,num+1+(int(file_index)-1)*num),test_x,np.full(num,int(file_index)))),
                                index=pd.date_range(start=start_time,
                                                    periods=num,freq=interval),columns=['sample_index','x','label'])

    return te_input
    


#database
def main(dbname,measurements,tags,dataset,query,host='localhost', port=8086):
    user = 'root'
    password = 'root'
    #dbname = 'demo'#数据库名称
    protocol = 'line'#行协议

    client = DataFrameClient(host, port, user, password, dbname)


    print("创建数据库: " + dbname)
    client.create_database(dbname)
    #print(dataset.shape[0])
    #print('!!!')
    #print("将DataFrame写入数据库")
    for i in range(dataset.shape[0]-1):

        client.write_points(dataset.iloc[i:i+1], measurements,{'classes':tags},protocol=protocol)
        #print("Waiting for data...")
        #time.sleep(0.2)


    if query == False:
        pass
    elif query == True:
        #print("查询")
        result=client.query('select * from Tenessee')#-------------------这里还需要进一步变通一下 满足不同的查询命令
                                                    #select * from Tenessee where class='training' #获取训练集
        print(result)
        np.save('D:/Documents/大创/zyl_data.npy',result)
    else:
        print("parameter 'query' is not valid")



    #print("删除数据库: " + dbname)
    #client.drop_database(dbname)


def parse_args():
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


now = '2021-02-28 22:30:25'


if __name__ == '__main__':
    args = parse_args()
    filepath = "D:/Documents/大创/TE_process/"
    index=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21']
    index_small = ['00']
    #注：此处没能找到比较好的处理时间的方法 待讨论
    timea=['2021-2-1','2021-3-2','2021-4-3','2021-5-4','2021-6-5','2021-7-6','2021-8-7','2021-9-8','2021-10-9','2021-11-10','2021-12-11','2021-1-12','2021-2-13','2021-3-14','2021-4-15','2021-5-16','2021-6-17','2021-7-18','2021-8-19','2021-9-20','2021-10-21']
    time2=['2020-2-1','2020-3-2','2020-4-3','2020-5-4','2020-6-5','2020-7-6','2020-8-7','2020-9-8','2020-10-9','2020-11-10','2020-12-11','2020-1-12','2020-2-13','2020-3-14','2020-4-15','2020-5-16','2020-6-17','2020-7-18','2020-8-19','2020-9-20','2020-10-21']
    #ss=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #print(ss)
    for i in index_small:
        # print('Waiting for another input....')

        #tr=tr_input(filepath,i,timea[(int(i)-1)],'0.05H')
        #te=te_input(filepath,i,time2[(int(i)-1)],'0.05H')
        te=te_input(filepath,i,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'0.05H')
        #print(te.iloc[0])
        #main(dbname='industrial_database',measurements='Tenessee',dataset=tr,tags='training',query=True,host=args.host, port=args.port)
        #print('Waiting for another input....')
        #time.sleep(2)
        main(dbname='industrial_database_te',measurements='Tenessee',dataset=te,tags='testing',query=True,host=args.host, port=args.port)
