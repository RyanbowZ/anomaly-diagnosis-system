#coding:utf-8

import socket
import time

class Server:
    def __init__(self,host,port):
        self.port = port
        self.host = host
        self.status = 0
        self.BUF_SIZE = 1024

    def createServer(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))

    def startServer(self):
        self.status = 1
        self.createServer()
        #设置接收的连接数为1
        self.server.listen(1)
        client, address = self.server.accept()
        while self.status == 1:  # 循环收发数据包，长连接
            data = client.recv(self.BUF_SIZE)
            text = data.decode()
            if text != "":
                print(text)  # python3 要使用decode
                #client.send("world".encode())
                #client.close() #连接不断开，长连接

if __name__ == "__main__":
    server = Server("localhost",8084)
    server.createServer()
    server.startServer()