# 多进程TCP客户机程序
# 服务器IP:192.168.0.104
# 客户机IP:192.168.0.102
import time
import numpy as np
from socket import *

serverName = "192.168.0.104"  # 服务器主机
serverPort = 6121         # 端口号
clientsocket = socket(AF_INET,SOCK_STREAM)      # 创建客户机套接字
clientsocket.connect((serverName,serverPort))   # 建立连接
## 发送请求报文并接收服务器的回复
fetch_file = "/myfile.html"  # 需要请求的文件
requestRow = "Get "+fetch_file+" HTTP/1.1\r\n"   # 请求行
firstRow = "Host:192.168.0.102\r\nUser-agent:Microsoft Edge/100.0.1185.36\r\nConnection:close\r\nAccept-language:ch\r\n\r\n"  # 首部行
requestMessages = requestRow+firstRow   # 请求报文（请求行+首部行）
print("请求报文发出时间:",time.strftime("%Y-%m-%d %H:%M:", time.localtime(time.time())),np.mod(time.time(),60),sep="")

start = time.perf_counter()                   # 记录发送请求报文的时间戳
clientsocket.send(requestMessages.encode())   # 发送请求报文
responseMessage = clientsocket.recv(1024)     # 接收服务器的回复
end = time.perf_counter()                     # 记录接收响应报文的时间戳
print("RTT:",end-start,"s")                   # 计算一个时延
print("响应报文：\n",responseMessage.decode(),sep = "")   # 控制台输出响应报文内容

## 生成本地html文件
f = open('localHtml.html','w')
message = responseMessage.decode()    # 报文解码
message = message.split("\r\n")       # 解析报文
content = message[-1]                 # 获取向服务器申请的文件
f.write(content)       # 保存到本地文件中
f.close()
## 关闭套接字
clientsocket.close()