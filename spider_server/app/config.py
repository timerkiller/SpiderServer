#-*- coding:utf-8 -*-

class serviceConfig(object):
    """
    服务器相关信息全局配置
    """
    #OBD服务器设置
    SERVICE_IP = "0.0.0.0"
    SERVICE_PORT = 25089
    MAX_LISTEN = 10000
    THREAD_NUM = 10
    THREAD_POOL_QUEUE = 1000

    #手机检测接口
    MOBILE_SERVICE_IP = "0.0.0.0"
    MOBILE_SERVICE_PORT = 25088
    MOBILE_MAX_LISTEN = 10000
    MOBILE_THREAD_NUM = 10
    #数据库相关配置
    DB_NAME = ''
    DB_HOST = ''
    DB_PORT = 0
    DB_USER = ''
    DB_PASSWORD = ''

    #redis相关配置
    REDIS_IP = ''
    REDIS_PORT = 0
    REDIS_USER = ''
    REDIS_PASSWORD = ''

class Config(object):
    base_url = 'http://www.ygdy8.net'
    base_new_url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_'
    base_japan_korean_url =  'http://www.ygdy8.net/html/gndy/rihan/list_6_'
    base_tail_url = '.html'

    regex_index_lastest = ''
    regex_lastest_movie_url = '</table><table width="100%" border="0" cellspacing="0" cellpadding="0" class="tbspan" style="margin-top:6px">.*?<a href="(.*?)".*?"ulink">(.*?)</a>'
    regex_lastest_movie_detail = '<div class="title_all"><h1><font.*?>(.*?)</font>.*?<ul>(.*?)<tr>.*?<img.*?src="(.*?)" alt="" />(.*?)<img border="0" src="(.*?)".*?<a href="(ftp://.*?)".*?</a>'
    regex_jp_kn_movie_url= ''
    regex_jp_kn_movie_detail = ''
