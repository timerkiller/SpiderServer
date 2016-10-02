#-*- coding:utf-8 -*-
__author__ = 'jclin'
import threading

import sys
import time
import math

if sys.version_info.major == 3:
    import queue as Queue
else:
    import Queue as Queue


'''
线程池的模拟实现
'''

class workThread(threading.Thread):
    '''
    线程体模块
    '''

    def __init__(self,task_queue):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.task_queue = task_queue
        self.start()
        self.idle = True

    def run(self):
        sleep_time = 0.02 #第一次无任务可做休息10ms
        multiply = 0
        while True:
            try:
                func,args,kwargs = self.task_queue.get(block = False)
                self.idle = False
                multiply = 0
                func(*args,**kwargs)
            except Queue.Empty:
                '''
                time.sleep(sleep_time * math.pow(2,multiply))
                self.idle = True
                multiply += 1
                '''
                time.sleep(sleep_time)
                continue
            except:
                print (sys.exc_info())
                raise

class threadPool(object):
    '''
    线程池实现
    '''

    def __init__(self,thread_num = 10, max_queue_len = 1000):
        self.max_queue_len = max_queue_len
        self.task_queue = Queue.Queue(max_queue_len) #任务等待队列
        self.threads = []
        self._create_pool(thread_num)

    def _create_pool(self,thread_num):
        for i in range(thread_num):
            thread_obj = workThread(self.task_queue)
            self.threads.append(thread_obj)

    def add_task(self,func,*args,**kwargs):
        '''
        添加任务
        '''
        try:
            self.task_queue.put((func,args,kwargs))
        except Queue.Full:
            print('threadPool queue full')
            raise
        return self.task_queue.qsize()

    def is_safe(self):
        return self.task_queue.qsize() < 0.9 * self.max_queue_len

    def wait_for_complete(self):
        '''
        等待提交到线程池的所有任务执行完毕
        '''
        while not self.task_queue.empty():
            time.sleep(1)
            all_idle = True
            for th in self.threads:
                if not th.idle:
                    all_idle = False
                    break
            if all_idle:
                break
            else:
                time.sleep(1)