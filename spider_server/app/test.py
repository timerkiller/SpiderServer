#coding=utf-8
import urllib
import urllib2
import re
from tool import Tool
if __name__ == '__main__':
    page = 1
    #url= 'http://www.ygdy8.net/html/gndy/dyzz/20160928/52066.html'
    # url = 'http://www.dytt8.net/html/gndy/dyzz/20161002/52104.html'
    url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_1.html'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
    headers = {'User-Agent': user_agent}
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        content = response.read()

        pattern = re.compile(
            '</table><table width="100%" border="0" cellspacing="0" cellpadding="0" class="tbspan" style="margin-top:6px">.*?<a href="(.*?)".*?"ulink">(.*?)</a>',
            re.S)
        items = re.findall(pattern, content)
        pageUrls = []
        #print content
        # pattern = re.compile('<div class="title_all"><h1><font.*?>(.*?)</font>.*?<ul>(.*?)<tr>.*?<img.*?src="(.*?)" alt="" />(.*?)<img border="0".*?<a href="(ftp://.*?)".*?</a>',re.S)
        # #pattern = re.compile('<a href="(ftp.*?)">',re.S)
        # print 'start find'
        # items = re.findall(pattern, content)
        print 'items len',len(items)
        for item in items:
            for data in item:
                print Tool.replace(data)
            print '\n'

    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason
