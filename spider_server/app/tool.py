#coding=utf-8
import re
# 处理页面标签类
import datetime
import time
from loglib.logApi import CSysLog
from django.utils import timezone
import chardet
class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>|  {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    removePonit = re.compile('&middot;')

    #获取发布时间
    releaseTime = re.compile('(\d{4}-\d{1,2}-\d{1,2}$)')

    @classmethod
    def replace(cls, dstStr):
        dstStr = re.sub(cls.removeImg, "", dstStr)
        dstStr = re.sub(cls.removeAddr, "", dstStr)
        dstStr = re.sub(cls.replaceLine, "\n", dstStr)
        dstStr = re.sub(cls.replaceTD, "\t", dstStr)
        dstStr = re.sub(cls.replacePara, "\n    ", dstStr)
        dstStr = re.sub(cls.replaceBR, "\n", dstStr)
        dstStr = re.sub(cls.removeExtraTag, "", dstStr)
        dstStr = re.sub(cls.removePonit, ".", dstStr)
        # strip()将前后多余内容删除
        return dstStr.strip()

    @classmethod
    def getReleaseTime(cls,dstStr):
        result = re.findall(cls.releaseTime,dstStr)
        if result:
            CSysLog.info(result[0])
            releaseTime = datetime.datetime.strptime(result[0],"%Y-%m-%d")
            return datetime.datetime(releaseTime.year,releaseTime.month,releaseTime.day)
        else:
            CSysLog.error('get release time error')
            return timezone.now()

    @classmethod
    def getStarScore(cls,dst_str):
        pattern = re.compile('(\d.\d)/.*? from')
        result = re.findall(pattern,dst_str)
        if(result):
            CSysLog.info(result[0])
            return float(result[0])
        else:
            return float('0.0')

    @classmethod
    def getMovieType(cls,dst_str):
        movie_type = re.compile('类.*?别　(.*?)<br />')
        result = re.findall(movie_type,dst_str)
        if result:
            CSysLog.info(result[0])
            return result[0]
        else:
            return '其他'

    @classmethod
    def getMovieContent(cls,dst_str):
        return cls.replace(dst_str)

    @classmethod
    def removeUnusefulText(cls,dst_str):
        try:
            movie_title_pattern = re.compile('《(.*?)》')
            result = re.findall(movie_title_pattern,dst_str.encode('utf-8'))
            if result:
                CSysLog.info(result[0])
                return result[0].decode('utf-8')
            else:
                return '其他'.encode('utf-8')
        except Exception,e:
            print e
