#coding=utf-8
import urllib2
import urllib
import re
import chardet
import time
from app.config import Config
from app.tool import Tool
from loglib.logApi import CSysLog
from app.database_operation.database_manager import DatabaseManager

class DyttSpider(object):
    '''
    电影天堂爬虫类，复杂电影天堂网站的视频资源爬取
    '''

    total_page = 2
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
    headers = {'User-Agent': user_agent}
    lastest_total_movies_urls = []
    movie_detail_items = []
    data_type_arr = ['lastest', 'classis']
    index_urls = {'lastest':[],'classis':[],'new_recommand':[],'classis_recommand':[]} #首页各个的URL集合
    index_movie_detail_items = {'lastest':[],'classis':[],'new_recommand':[],'classis_recommand':[]} #首页各个电影资源详情的集合

    # 传入某一页的索引获得页面代码

    class DataType:
        HOME_PAGE = 0x01#主页数据
        LASTEST_DATA_PAGE = 0x02#最新影片的数据
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
            fail_time = 0
            while True:
                try:
                    if fail_time > 5:
                        return None
                    request = urllib2.Request(pageUrl, headers = cls.headers)
                    response = urllib2.urlopen(request,None,3)
                    pageCode = response.read()
                    encodeType = chardet.detect(pageCode)['encoding']
                    if encodeType == 'ISO-8859-2':
                        pageCode = pageCode.decode('ISO-8859-2', 'ignore').encode('utf-8')
                    elif encodeType == 'gbk' or encodeType == 'GBK':
                        pageCode = pageCode.decode('gbk', 'ignore').encode('utf-8')
                    elif encodeType == 'gb2312' or encodeType == 'GB2312':
                        pageCode = pageCode.decode('gb2312', 'ignore').encode('utf-8')
                    else:
                        CSysLog.error('encode type not add %s'%(encodeType))
                    return pageCode
                except Exception,e:
                    CSysLog.warn('get page error reason: %s'%(e))
                    fail_time +=1
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"connect website faild", e.reason
                return None

    @classmethod
    def getPageUrlRes(cls,url,regex_pattern):
        '''
        获取当前页面里面的对应的所有电影链接
        :param url:
        :return:
        '''
        pageCode = cls.getPage(url)
        if not pageCode:
            CSysLog.error("load page failed....")
            return False
        pattern = re.compile(regex_pattern,re.S)
        items = re.findall(pattern, pageCode)
        for item in items:
            url = Tool.replace(item[0])
            title =Tool.replace(item[1])
            cls.lastest_total_movies_urls.append([url.strip(), title.strip()])
        return True

    @classmethod
    def get_movie_detail_res(cls,url):
        '''
        获取当前电影页面对应的详细信息
        :param url:
        :return:
        '''
        CSysLog.info('URL:%s',url)

        pageCode = cls.getPage(url)
        if not pageCode:
            CSysLog.error( "load page failed....")
            return None
        try:
            pattern = re.compile(Config.regex_lastest_movie_detail,re.S)
            #这里还需要详细解析
            items = re.findall(pattern, pageCode)
            for item in items:
                movie_detail = {}
                movie_detail['title'] = Tool.replace(item[0])
                movie_detail['releaseTime'] = Tool.replace(item[1])
                movie_detail['majorPicUrl'] = Tool.replace(item[2])
                movie_detail['content'] = item[3]
                movie_detail['summaryPicUrl'] = Tool.replace(item[4])
                movie_detail['ftpUrl'] = Tool.replace(item[5])
                return movie_detail#因为每个资源页面只有一项，所以直接返回第一个就可以了
        except:
            CSysLog.info('regex parse failed')
            return None

    @classmethod
    def get_lastest_all_movies_res(cls):
        for i in range(1,cls.total_page):
            url = Config.base_new_url + str(i) + Config.base_tail_url
            result = cls.getPageUrlRes(url,Config.regex_lastest_movie_url)
            if not result:
                CSysLog.error( 'Get page:%d url failed '%(i))

    @classmethod
    def print_lastest_total_movie_url(cls):
        CSysLog.info( 'Total movie url(%d)' % (len(cls.lastest_total_movies_urls)))
        # for item in cls.lastest_total_movies_urls:
        #     print 'Url:%s Title:%s'%(item[0],item[1])

    @classmethod
    def get_lastest_all_movies_detail(cls):
        CSysLog.info( 'Total movie url(%d)'%(len(cls.lastest_total_movies_urls)))
        for item in cls.lastest_total_movies_urls:
            url = Config.base_url+item[0]
            result = cls.get_movie_detail_res(url)
            if not result:
                CSysLog.error( 'get url :%s failed'%(url))
            else:
                cls.movie_detail_items.append(result)

    @classmethod
    def print_lastest_all_movies_detail(cls):
        CSysLog.info( 'movie_detail_items %d'%(len(cls.movie_detail_items)))
        for item in cls.movie_detail_items:
            CSysLog.info( 'Title:%s ReleaseTime:%s majorPicUrl:%s summaryPicUrl:%s FtpURL:%s'%(item['title'],item['releaseTime'],item['majorPicUrl'],item['summaryPicUrl'],item['ftpUrl']))

    @classmethod
    def print_all_movies_detail(cls,movie_list):
        CSysLog.info('movie_list len :%d'%(len(movie_list)))
        for item in movie_list:
            CSysLog.info( 'Title:%s ReleaseTime:%s majorPicUrl:%s summaryPicUrl:%s FtpURL:%s    \nContent: %s '%(item['title'],item['releaseTime'],item['majorPicUrl'],item['summaryPicUrl'],item['ftpUrl'],item['content']))


    @classmethod
    def getIndexData(cls):
        '''
        爬取首页的最新电影以及日韩，以及推荐等等
        :return:
        '''
        cls.index_urls = {'lastest': [], 'classis': [], 'new_recommand': [], 'classis_recommand': []}  # 首页各个的URL集合
        cls.index_movie_detail_items = {'lastest': [], 'classis': [], 'new_recommand': [],'classis_recommand': []}  #首页各个电影资源详情的集合

        # 获取更新推荐数据
        data_type_array = ['lastest','classis']
        for data_type in data_type_array:
            cls.getHomePageUrls(Config.base_url,Config.regex_home_page_url[data_type],data_type)
            #cls.printHomePageUrls(data_type)
            cls.getHomePageMovieDetail(data_type)
            #cls.print_all_movies_detail(cls.index_movie_detail_items[data_type])


    @classmethod
    def printHomePageUrls(cls,data_type):
        for item in cls.index_urls[data_type]:
            CSysLog.info('Index type:%s movies: Url:%s Title:%s'%(data_type,item[0],item[1]))

    @classmethod
    def getHomePageMovieDetail(cls, data_type):
        for data in cls.index_urls[data_type]:
            url = Config.base_url + data[0]
            #CSysLog.info(url)
            result = cls.get_movie_detail_res(url)
            if not result:
                CSysLog.error( 'get url :%s failed'%(url))
                continue
            else:
                cls.index_movie_detail_items[data_type].append(result)

    @classmethod
    def getHomePageUrls(cls,url,patteren,data_type):
        '''
        获取主页相应的栏的影片URL
        :param url:
        :param patteren:
        :param data_type: lastest:最新影片栏，classis:迅雷资源栏,
        :return:
        '''
        pageCode = cls.getPage(url)
        if not pageCode:
            CSysLog.error("load page failed....")
            return False
        pattern = re.compile(patteren, re.S)
        items = re.findall(pattern, pageCode)
        for item in items:
            url = Tool.replace(item[0])
            title = Tool.replace(item[1])
            cls.index_urls[data_type].append([url.strip(), title.strip()])

    @classmethod
    def write_to_database(cls,data_type):
        '''
        将所有视频数据写入数据库，因为爬虫更新不会太频繁去更细你，所以这里无需用另外一个线程去更新数据库数据
        :return:
        '''
        if data_type == cls.DataType.HOME_PAGE:
            if len(cls.index_movie_detail_items) != 0:
                result_data = cls.parse_index_movie_detail_item(cls.index_movie_detail_items)
                DatabaseManager.get_movie_model_instance().set_array_movies_data(result_data,cls.DataType.HOME_PAGE)
            else:
                CSysLog.error('No index data yet, please check the spider')
        elif data_type == cls.DataType.LASTEST_DATA_PAGE:
            if len(cls.movie_detail_items) != 0:
                DatabaseManager.get_movie_model_instance().set_array_movies_data(cls.movie_detail_items,cls.DataType.LASTEST_DATA_PAGE)
            else:
                CSysLog.error('No lastest data yet, please check the spider')
        elif data_type == cls.DataType.JP_KO_DATA_PAGE:
            pass
        elif data_type == cls.DataType.EUR_AMER_DATA_PAGE:
            pass
        else:
            CSysLog.error('Data type error!!!!')

    @classmethod
    def parse_index_movie_detail_item(cls,movie_list):
        pass
        result = []
        for data_type in cls.data_type_arr:
            for movie in movie_list[data_type]:
                movie_detail ={}
                movie_detail['title'] = movie['title']
                movie_detail['release_time'] = Tool.getReleaseTime(movie['releaseTime'])
                movie_detail['major_img_url'] = movie['majorPicUrl']
                movie_detail['movie_star_score'] = Tool.getStarScore(movie['content'])
                movie_detail['movie_type'] = Tool.getMovieType(movie['content'])
                movie_detail['movie_classify'] = 0x01
                movie_detail['movie_classify_child'] = data_type
                movie_detail['summary_img_url'] = movie['summaryPicUrl']
                movie_detail['content'] = Tool.getMovieContent(movie['content'])
                movie_detail['ftp_url'] = movie['ftpUrl']
                result.append(movie_detail)
        return result


    @classmethod
    def start_all(cls):
        #获取最新电影的所有链接
        cls.get_lastest_all_movies_res()
        cls.print_lastest_total_movie_url()

        #在获取链接的基础上，获取所有的最新电影详情
        cls.get_lastest_all_movies_detail()
        cls.print_all_movies_detail(cls.movie_detail_items)

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
        if data_type == cls.DataType.HOME_PAGE:
            cls.getIndexData()