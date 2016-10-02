#coding=utf-8
import time,datetime
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
class CMyTools(object):

    @classmethod
    def timestampToDatetime(cls,value):
        '''
        时间戳转换成datetime,
        Args:
            value: int的时间戳
        Returns
            dt: 字符串型的日期
        '''
        format = '%Y-%m-%d %H:%M:%S'
        value = time.localtime(value)
        dtstring = time.strftime(format, value)
        dt = datetime.datetime.strptime(dtstring,format)
        return dt

    @classmethod
    def datetimeToTimestamp(cls,dt):
        '''
        datetime转成时间戳
        Args:
            dt: int的时间戳
        Returns
            value: 返回时间戳
        '''

        time.strptime(dt, '%Y-%m-%d %H:%M:%S')
        s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
        return int(s)
    @classmethod
    def datetimeToInt(cls,date):
        strTime = date.strftime("%Y-%m-%d %H:%M:%S")
        return CMyTools.datetimeToTimestamp(strTime)

    @classmethod
    def pagination_display(cls,itemList, currentPage,each_page = 8):
        paginator = Paginator(itemList,each_page)
        try:
            page = int(currentPage)
        except ValueError:
            page = 1
        try:
            newItemList = paginator.page(page)
        except (EmptyPage, InvalidPage):
            newItemList = paginator.page(paginator.num_pages)
        return newItemList

if __name__ == '__main__':
  d = CMyTools.datetimeToTimestamp('2016-09-30 06:54:40')
  print d
  s = CMyTools.timestampToDatetime(2432888820)
  print s