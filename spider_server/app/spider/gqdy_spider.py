#coding=utf-8
from app.spider.base_spider import BaseSpider
from loglib.logApi import CSysLog
from app.tool import Tool
from app.database_operation.database_manager import DatabaseManager

import re
class GqdySpider(BaseSpider):

    total_page = 150#一共152页
    GQDY_INDEX_URL = "http://www.1234hdhd.com"
    GQDY_MOVIE_LIST_URL = GQDY_INDEX_URL+"/htm/list_0_0_0_0_time1_"

    index_pattern_newest = re.compile('<li><a href="(.*?)".*?class="m_name">(.*?)</span></a></li>',re.S)
    index_pattern_recommand = re.compile('<li><span><font.*?<a href="(.*?)".*?target="_blank">(.*?)</a></div></li>',re.S)

    movie_list_pattern = re.compile('<li><a href="(/htm/movie\d.*?)" target="_blank">.*?<span>(.*?)</span>',re.S)
    # movie_detail_pattern =re.compile('<div class="movie_pic"><img src="(图片地址".*?<div class="movie_info">.*?<stro标题(.*?)</strong>.*?<a href=".*?>(.*?)</a>.喜剧片ffffffffffffffffffffffffffffffffffffffffffffffffffff演员fffffffffffffffffffffffffffffffffffffff国家ffffffffffffffffffffffffffffffffffff年份ffff更新时间ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff下载地址fffffffffffffffffffffffffffffffffffffffffff内容fffffffffff)
    movie_detail_pattern =    re.compile('<div class="movie_pic"><img src="(.*?)".*?<div class="movie_info">.*?<strong>(.*?)</strong></div></div>.*?<a href=".*?">(.*?)</a></div></div>.*?><a href="/htm/search_actor.*?">(.*?)</a>.*?</div></div>.*?<a href=.*?>(.*?)</a></div></div>.*?<a href=.*?>(.*?)</a>(.*?)</div></div>.*?<div style="padding:9px; line-height:20px;">.*?<a href="(http://.*?)" target="_blank">.*?<div class="text">(.*?)</div>',re.S)
    # movie_pic_address_pattern=re.compile('<div class="movie_pic"><img src="(.*?)".*?<div class="movie_info">.*?<strong>(.*?)</strong></div></div>.*?<a href=".*?">(.*?)</a></div></div>.*?><a href="/htm/search_actor.*?">(.*?)</a>.*?</div></div>.*?<a href=.*?>(.*?)</a></div></div>.*?<a href=.*?>(.*?)</a>(.*?)</div></div>.*?<div style="padding:9px; line-height:20px;">.*?<a href="(http://.*?)" target="_blank">.*?<div class="text">(.*?)</div>',re.S)
    title_pattern = re.compile('',re.S)
    movie_type_pattern = re.compile('<div class="movie_info">.*?<a href=".*?">(.*?)</a></div></div>',re.S)

    index_movie_url = {'newest':[],'recommend':[],'all_data':[]}
    index_movie = {'newest':[],'recommend':[],'all_data':[]}

    @classmethod
    def getPageUrl(cls, pattern, url, data_type):
        pageCode = cls.getPage(url)
        if pageCode == None:
            CSysLog.error("get page index error url:%s"%(url))
            return
        items = re.findall(pattern, pageCode)
        for item in items:
            url = Tool.replace(item[0])
            title = Tool.replace(item[1])
            cls.index_movie_url[data_type].append([url.strip(), title.strip()])

    @classmethod
    def getMovieDetail(cls,pattern,url,data_type):
        pageCode = cls.getPage(url)
        #print pageCode
        if pageCode == None:
            CSysLog.error("get page index error url:%s" % (url))
            return

        # items = re.findall(cls.movie_pic_address_pattern,pageCode)
        # for item in items:
        #     print item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8]
        items = re.findall(pattern, pageCode)
        for item in items:
            movie_detail={}
            movie_detail['image_url'] =item[0] #Tool.replace(item[0])
            movie_detail['title'] =item[1] #Tool.replace(item[0])
            movie_detail['movie_type'] =item[2] #Tool.replace(item[0])
            movie_detail['actor'] =item[3] #Tool.replace(item[0])
            movie_detail['country'] =item[4] #Tool.replace(item[0])
            movie_detail['update_time'] =item[5] #Tool.replace(item[0])
            movie_detail['release_time'] =item[6] #Tool.replace(item[0])
            movie_detail['download_url'] =item[7] #Tool.replace(item[0])
            movie_detail['content'] =item[8] #Tool.replace(item[0])
            cls.index_movie[data_type].append(movie_detail)

    @classmethod
    def getIndexUrl(cls):
        cls.getPageUrl(cls.index_pattern_newest, cls.GQDY_INDEX_URL, 'newest')
        cls.getPageUrl(cls.index_pattern_recommand, cls.GQDY_INDEX_URL, 'recommend')
        CSysLog.info('Get index movie url done')
        cls.print_index_data()

    @classmethod
    def getAllDataUrl(cls):
        for pageIndex in range(1,cls.total_page):
            movie_url = cls.GQDY_MOVIE_LIST_URL+str(pageIndex) +".htm"
            CSysLog.info("all_data url :%s"%(movie_url))
            cls.getPageUrl(cls.movie_list_pattern,movie_url,'all_data')

        for item in cls.index_movie_url['all_data']:
            CSysLog.info("all_data Url: %s  Title: %s" % (item[0], item[1]))

    @classmethod
    def getAllDataMovieDetail(cls):
        for urldetail in cls.index_movie_url['all_data']:
            movie_detail_url = cls.GQDY_INDEX_URL+urldetail[0]
            CSysLog.info( 'url:%s'%movie_detail_url)
            cls.getMovieDetail(cls.movie_detail_pattern,movie_detail_url,'all_data')

        CSysLog.info("get movie detail as below:")
        for item in cls.index_movie['all_data']:
            print item['title'],item['release_time']

    @classmethod
    def print_index_data(cls):
        for item in cls.index_movie_url['newest']:
            CSysLog.info("newest Url: %s  Title: %s"%(item[0],item[1]))
        for item in cls.index_movie_url['recommend']:
            CSysLog.info("recommand Url: %s  Title: %s"%(item[0],item[1]))

    @classmethod
    def get_movie_detail_data(cls,movie_list):
        data_objects =[]
        for movie in movie_list:
            movie_detail = {}
            movie_detail['title'] = Tool.getGqdyTitle(movie['title'])
            movie_detail['release_time'] = Tool.getGqdyReleaseTime(movie['release_time'])
            movie_detail['major_img_url'] = movie['image_url']
            movie_detail['movie_star_score'] = "0.0"
            movie_detail['movie_type'] = movie['movie_type']
            movie_detail['movie_classify'] = cls.DataType.GQDY_WEBSITE_ALL_DATA
            movie_detail['movie_classify_child'] = 0
            movie_detail['summary_img_url'] = ""
            movie_detail['update_time'] = movie['update_time']
            movie_detail['country'] = movie['country']
            movie_detail['content'] =movie['content']
            movie_detail['actor'] = movie['actor']
            movie_detail['download_url'] = movie['download_url']
            movie_detail['movie_source'] = 'gqdy'
            data_objects.append(movie_detail)
        return data_objects

    @classmethod
    def write_all_data_to_database(cls):
        result = cls.get_movie_detail_data(cls.index_movie['all_data'])
        DatabaseManager.get_movie_model_instance().set_array_movies_data(result, cls.DataType.GQDY_WEBSITE)
        CSysLog.info("write all data to data base done")

    @classmethod
    def start(cls,data_type):
        if data_type == 0x00:#获取首页的movie URL链接
            cls.getIndexUrl()

            cls.getIndexMovieDetail()
        elif data_type == 0x01:#获取全部MOVIE的URL链接
            try:
                cls.getAllDataUrl()
                CSysLog.info('get all data url done')
                cls.getAllDataMovieDetail()
                CSysLog.info("get all data moveidetail done")
            except Exception,e:
                print e
        else:
            cls.getAllDataMovieDetail()








