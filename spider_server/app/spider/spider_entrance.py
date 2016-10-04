#-*- coding:utf-8 -*-
import time
import re
import threading
from loglib.logApi import CSysLog
from app.spider.dytt_spider import DyttSpider

class SpiderThread(object):

    server_run_flag = True
    __thread_pool = None
    first_start = True
    m_mutex = threading.Lock()

    @classmethod
    def register_thread_pool(cls,threadpool):
        cls.__thread_pool = threadpool

    @classmethod
    def close(cls):
        cls.server_run_flag = False

    @classmethod
    def run(cls):
        '''
        爬虫运行体
        '''
        while cls.server_run_flag:
            #第一次启动的时候，因为数据库里没数据，所以进行全网爬数据
            if cls.first_start:
                cls.first_start = False
                DyttSpider.start(0x01)
                try:
                    DyttSpider.write_to_database(DyttSpider.DataType.HOME_PAGE)
                except Exception,e:
                    CSysLog.info('write data to datebase error :%s ',e)
            #需要每隔一定时间去爬取相应的首页数据
            time.sleep(2000)

    @classmethod
    def start(cls):
        cls.__thread_pool.add_task(cls.run)