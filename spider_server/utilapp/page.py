#coding=utf-8
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage

__author__ = 'jclin'
#分页类
class CPage(object):
    def __init__(self,obj,perPage):
        self.obj = obj
        self.perPage = perPage
        self.counts = len(obj)

    def getPageCounts(self):
        if self.counts % self.perPage > 0:
            pageAll = self.counts / self.perPage +1
        else:
            pageAll = self.counts / self.perPage
        return  pageAll

    def getPageDate(self,page):
        start = self.perPage * page - 1
        end = start + self.perPage
        if start > self.counts:
            items = []
        elif end > self.counts:
            items = self.obj[start:self.counts]
        else:
            items = self.obj[start:end]
        return items

class CPageHelper(object):
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
        return newItemList,paginator.num_pages

