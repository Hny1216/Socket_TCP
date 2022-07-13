# 多进程TCP服务器程序
# 服务器IP:192.168.0.104
# 客户机IP:192.168.0.102
import time
import numpy as np
from socket import *
import threading
def TCPServer(connectionSocket,address):
    # 将实验1中的服务器程序包装成函数
    try:
        # 接收请求报文并读取文件
        message = connectionSocket.recv(1024).decode()  # 接收客户机的请求报文
        print("接收到请求报文的时间:", time.strftime("%Y-%m-%d %H:%M:", time.localtime(time.time())), np.mod(time.time(), 60), sep="")
        print("已接收到请求报文：\n", message)
        filename = message.split()[1]  # 解析请求报文，获取文件名
        with open(filename[1:], "r") as f:
            content = f.read()  # 根据文件名读取文件内容
        ## 生成响应报文（状态行+首部行+文件内容）
        stateRow = "HTTP/1.1 200 OK\r\n"  # 状态行
        firstRow = "Connection close\r\nDate:" + time.strftime("%Y-%m-%d", time.localtime(
            time.time())) + "\r\n服务器:Apache/1.3.0 (Windows)\r\nLast-Modified:Wedn,13 April 2022\r\nContent-Length:" + str(
            len(content)) + "\r\nContent-Type:html\r\n\r\n"  # 首部行
        outputdata = stateRow + firstRow + content  # 响应报文 = 状态行+首部行+文件内容
        time.sleep(10)    # 使服务器睡眠10秒，模拟堵塞，便于实现多次请求
        connectionSocket.send(outputdata.encode())  # 返回响应报文字节流
        connectionSocket.close()  # 关闭TCP连接
    except IOError:  # 抛出异常
        print("[ERROR]The file being fetched is not existed.")
        with open("error.html", "r") as f:    # 出现异常则返回错误的网页(404)
            content = f.read()
        ## ## 生成响应报文（状态行+首部行+文件内容）
        stateRow = "HTTP/1.1 404 Not Found\r\n"  # 状态行
        firstRow = "Connection close\r\nDate:" + time.strftime("%Y-%m-%d", time.localtime(
            time.time())) + "\r\n服务器:Apache/1.3.0 (Windows)\r\nLast-Modified:Wedn,13 April 2022\r\nContent-Length:" + str(
            len(content)) + "\r\nContent-Type:html\r\n\r\n"  # 首部行
        outputdata = stateRow + firstRow + content  # 响应报文 = 状态行+首部行+文件内容
        time.sleep(10)   # 使服务器睡眠10秒，模拟堵塞，便于实现多次请求
        connectionSocket.send(outputdata.encode())  # 返回错误响应字节流
        connectionSocket.close()   # 关闭TCP连接


serverSocket = socket(AF_INET, SOCK_STREAM)  # 生成服务器的TCP连接套接字
serverPort = 6121  # 端口号
serverSocket.bind(("", serverPort))  # 绑定服务器套接字和端口号
serverSocket.listen(10)    # 聆听客户连接
while True:
    connectionSocket,address = serverSocket.accept()    # 等待连接
    thread = threading.Thread(target=TCPServer, args=(connectionSocket,address))    # 加入线程，多线程进行处理
    thread.start()

