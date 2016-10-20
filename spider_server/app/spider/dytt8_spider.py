#coding=utf-8
from app.spider.base_spider import BaseSpider
import re

class Dytt8Spider(BaseSpider):

    movie_url = "www.dytt.com/fenlei/15.html"
    teleplay_url = "www.dytt.com/fenlei/16.html"
    carton_url = "www.dytt.com/fenlei/7.html"
    varshow_url = "www.dytt.com/fenlei/8.html"
    movie3d_url = "http://www.dytt.com/fenlei/21.html"
    movie_new_url = "http://www.dytt.com/fenlei/18.html"

    movie_list_pattern = re.compile('<li><p class="s1"><a href="(.*?)" title="(.*?)".*?</p></li>',re.S)
    #                                                              image       title               year                    type                    actor                   region                 update_time                                           address1
    movie_detail_pattern = re.compile('<div class="pic"><img src="(.*?)" alt="(.*?)".*?<li><span>(.*?)</li>.*?<li><span>(.*?)</li>.*?<li><span>(.*?)</li>.*?<li><span>(.*?)</li>.*?<li><span>(.*?)</li>.*?<h4>资源下载地址1</h4>.*?GvodUrls =.*?"(.*?)";')