#coding=utf-8
import urllib
class UrlUtils(object):

    @classmethod
    def encode(cls,url):
        '''
        需要编码的url链接
        :param url:
        :return:
        '''
        return urllib.quote(url)

    @classmethod
    def decode(cls,url):
        return urllib.unquote(url)