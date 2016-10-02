#coding=utf-8

import threading

from app import pool
from app.config import serviceConfig
from app.spider.spider_enterance import SpiderThread


class BusinessThreadEntrance(object):
    objs_locker =  threading.Lock()
    is_server_start = False

    @classmethod
    def start(cls):
        cls.objs_locker.acquire()
        if cls.is_server_start:
            return
        else:
            cls.is_server_start = True
        cls.objs_locker.release()

        thread_pool = pool.threadPool(serviceConfig.THREAD_NUM,serviceConfig.THREAD_POOL_QUEUE)
        SpiderThread.register_thread_pool(thread_pool)
        SpiderThread.start()
