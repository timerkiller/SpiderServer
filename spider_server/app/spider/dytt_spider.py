#coding=utf-8
import urllib2
import urllib
import re
from app.config import Config
from app.tool import Tool
from loglib.logApi import CSysLog

class DyttSpider(object):
    '''
    电影天堂爬虫类，复杂电影天堂网站的视频资源爬取
    '''

    total_page = 2
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
    headers = {'User-Agent': user_agent}
    total_movies_urls = []
    movie_detail_items = []
    # 传入某一页的索引获得页面代码

    class DataType:
        HOME_PAGE = 0x01#主页数据
        NEWEST_DATA_PAGE = 0x02#最新的数据
        JP_KO_DATA_PAGE = 0x03#日韩电影数据
        EUR_AMER_DATA_PAGE = 0x04#欧美电影数据

    @classmethod
    def set_total_page(cls,page):
        '''
        设置爬取页数
        :param page: 爬取的页数
        :return:
        '''
        if type(page) != 'int':
            return False

        cls.total_page = page
        return True

    @classmethod
    def getPage(cls, pageUrl):
        '''
        获取某个网页的信息，后面可以考虑使用scray框架
        :param pageUrl:
        :return: 返回获取到的网页信息
        '''
        try:
            request = urllib2.Request(pageUrl, headers = cls.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"connect website faild", e.reason
                return None

    @classmethod
    def getPageUrlRes(cls,url):
        '''
        获取当前页面里面的对应的所有电影链接
        :param url:
        :return:
        '''
        pageCode = cls.getPage(url)
        if not pageCode:
            CSysLog.error("load page failed....")
            return False
        pattern = re.compile(Config.regex_lastest_movie_url,re.S)
        items = re.findall(pattern, pageCode)
        for item in items:
            url = Tool.replace(item[0])
            title =Tool.replace(item[1])
            cls.total_movies_urls.append([url.strip(), title.strip()])
        return True

    @classmethod
    def get_movie_detail_res(cls,url):
        '''
        获取当前电影页面对应的详细信息
        :param url:
        :return:
        '''
        pageCode = cls.getPage(url)
        if not pageCode:
            CSysLog.error( "load page failed....")
            return None
        pattern = re.compile(Config.regex_lastest_movie_detail,re.S)
        #这里还需要详细解析
        items = re.findall(pattern, pageCode)
        for item in items:
            movie_detail = {}
            movie_detail['title'] = Tool.replace(item[0])
            movie_detail['releaseTime'] = Tool.replace(item[1])
            movie_detail['majorPicUrl'] = Tool.replace(item[2])
            movie_detail['content'] = Tool.replace(item[3])
            movie_detail['summaryPicUrl'] = Tool.replace(item[4])
            movie_detail['ftpUrl'] = Tool.replace(item[5])
            cls.movie_detail_items.append(movie_detail)
        return True

    @classmethod
    def get_all_movies_res(cls):
        for i in range(1,cls.total_page):
            url = Config.base_new_url + str(i) + Config.base_tail_url
            result = cls.getPageUrlRes(url)
            if not result:
                CSysLog.error( 'Get page:%d url failed '%(i))

    @classmethod
    def print_total_movie_url(cls):
        CSysLog.info( 'Total movie url(%d)' % (len(cls.total_movies_urls)))
        # for item in cls.total_movies_urls:
        #     print 'Url:%s Title:%s'%(item[0],item[1])

    @classmethod
    def get_all_movies_detail(cls):
        CSysLog.info( 'Total movie url(%d)'%(len(cls.total_movies_urls)))
        for item in cls.total_movies_urls:
            url = Config.base_url+item[0]
            result = cls.get_movie_detail_res(url)
            if not result:
                CSysLog.error( 'get url :%s failed'%(url))

    @classmethod
    def print_all_movies_detail(cls):
        CSysLog.info( 'movie_detail_items %d'%(len(cls.movie_detail_items)))
        for item in cls.movie_detail_items:
            CSysLog.info( 'Title:%s ReleaseTime:%s majorPicUrl:%s summaryPicUrl:%s FtpURL:%s'%(item['title'],item['releaseTime'],item['majorPicUrl'],item['summaryPicUrl'],item['ftpUrl']))

    @classmethod
    def start_all(cls):
        #获取最新电影的所有链接
        cls.get_all_movies_res()
        cls.print_total_movie_url()

        #在获取链接的基础上，获取所有的电影详情
        cls.get_all_movies_detail()
        cls.print_all_movies_detail()

    @classmethod
    def start(cls,data_type):
        '''
        根据类型类启动爬虫
        HOME_PAGE = 0x01#主页数据,需要每隔一定时间去爬取，获取更新数据
        NEWEST_DATA_PAGE = 0x02#最新的数据
        JP_KO_DATA_PAGE = 0x03#日韩电影数据
        EUR_AMER_DATA_PAGE = 0x04#欧美电影数据

        :param data_type:
        :return:
        '''
        pass