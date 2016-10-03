#coding=utf-8
import re
# 处理页面标签类
import datetime
class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
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
        # strip()将前后多余内容删除
        return dstStr.strip()

    @classmethod
    def getReleaseTime(cls,dstStr):
        result = re.findall(cls.releaseTime,dstStr)
        if result:
            return result[0]
        else:
            return datetime.datetime.today().strftime('%Y-%m-%d')

    @classmethod
    def getStarScore(cls,dst_str):
        pass

    @classmethod
    def getMovieType(cls,dst_str):
        pass

    @classmethod
    def getMovieContent(cls,dst_str):
        pass