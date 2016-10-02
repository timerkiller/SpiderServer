__author__ = 'jclin'
from socket import *
host = '127.0.0.1'
port = 25089
bufsize = 1024
import  time
addr = (host,port)
client = socket(AF_INET,SOCK_STREAM)
client.connect(addr)
client.send("hello world".encode())
client.close()