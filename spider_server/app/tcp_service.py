#-*- coding:utf-8 -*-
__author__ = 'jclin'
import socket
import select
import time
import sys
import threading
if sys.version_info.major == 3:
    import queue as Queue
else:
    import Queue as Queue

from loglib.logApi import CSysLog

class TcpServer(object):
    def __init__(self,thread_pool,is_blocking = False):
        self.local_ip = '0.0.0.0'
        self.local_port = 0
        self.server_fd = -1
        self.is_blocking = is_blocking
        self.inputs = []
        self.outputs = []
        self.delete_socket = [] #待删除队列
        self.thread_pool = thread_pool
        self.output_message = {}
        self.out_message_queue_len = 100
        self.listen_num = 10
        self.m_mutex = threading.Lock()
        self.thread = None
        self.server_on = True

    def delete_socket_queue(self):
        return self.delete_socket

    def set_listen_num(self,listen_num):
        self.listen_num = listen_num

    def set_local_port(self,port):
        self.local_port = port

    def set_local_ip(self,ip):
        self.local_ip = ip

    def send_message(self,socket_fd,message):
        '''
        对外接口
        加入发送队列
        '''
        self.m_mutex.acquire()
        if socket_fd in self.output_message:
            message_queue = self.output_message[socket_fd]
            message_queue.put(message)
        self.m_mutex.release()

    def init_socket(self):
        try:
            self.server_fd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.server_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except:
            CSysLog.error("socket Init error")

    def register_handler(self,func):
        self.handler = func

    def start_server(self):
        self.init_socket()
        self.server_fd.bind((self.local_ip,self.local_port))
        self.server_fd.listen(self.listen_num)
        if self.is_blocking:
            self.poll_message()
        else:
            self.thread = threading.Thread(target=self.poll_message)
            self.thread.start()
            # self.thread_pool.add_task(self.poll_message)

    def close_server(self):
        self.server_on = False

    def poll_message(self):
        self.inputs.append(self.server_fd)
        while self.inputs and self.server_on:
            timeout = 20
            self.m_mutex.acquire()
            for s in self.delete_socket:
                #删除清除队列中的
                if s in self.inputs:
                    self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                if s in self.output_message:
                    temp_queue = self.output_message.pop(s)
                    del temp_queue
                self.delete_socket.remove(s)
                print('close socket s ',s)
                s.close()

            self.m_mutex.release()
            try:
                readable,writeable,exceptional = select.select(self.inputs,self.outputs,self.inputs,timeout)
            except:
                CSysLog.error('select error')
                continue
            # if not(readable or writeable or exceptional):
            #     CSysLog.info('select time out')
            else:
                for s in readable:
                    if s is self.server_fd:#处理新连接
                        connection,client_address = s.accept()
                        CSysLog.info('connect from :%s',str(client_address))
                        self.m_mutex.acquire()
                        self.inputs.append(connection)
                        self.outputs.append(connection)
                        message_que = Queue.Queue(self.out_message_queue_len)
                        self.output_message.setdefault(connection,message_que)
                        self.m_mutex.release()
                    else:
                        self.handler(s,self.delete_socket)
                for s in writeable:
                    #发送队列
                    if s in self.output_message:
                        message_queue = self.output_message[s]
                        try:
                            data = message_queue.get(block = False)
                            s.send(data)
                        except:
                            pass

                for s in exceptional:
                    CSysLog.info('exception conditon on %s',s.getpeername())
                time.sleep(0)
