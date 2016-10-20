#coding=utf-8
import time
import urllib2
import urllib
from loglib.logApi import CSysLog
import chardet
from utilapp.url_util import UrlUtils
class BaseSpider(object):

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
    headers = {'User-Agent': user_agent}

    # 传入某一页的索引获得页面代码
    class DataType:
        HOME_PAGE = 0x00#主页数据
        NEW_MOV = 0x01#最新影片的数据
        EUR_US_MOV = 0x02  # 欧美电影数据
        JAP_KOR_MOV = 0x03#日韩电影数据
        CH_TELEPLAY = 0x04  # 国内电视剧
        VAIRETY_SHOW = 0x05  # 综艺
        US_TELEPLAY = 0x06  # 美剧
        STAR_SCORE = 0x07  # 评分最高

        GQDY_WEBSITE = 0x100#
        GQDY_WEBSITE_ALL_DATA = 0x101#
        GQDY_WEBSITE_INDEX_DATA= 0x102

    @classmethod
    def getPage(cls, pageUrl):
        '''
        获取某个网页的信息，后面可以考虑使用scray框架
        :param pageUrl:
        :return: 返回获取到的网页信息
        '''
        time.sleep(1)#每隔一秒去读取，太快你懂的
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
                    elif encodeType=='utf-8' or encodeType == 'UTF-8':
                        #return pageCode
                        pageCode = pageCode.decode('utf-8','ignore').encode('utf-8')
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
    def url_encode(cls,url):
        return UrlUtils.encode(url)