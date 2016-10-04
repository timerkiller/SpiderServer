# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.db import models

class MovieModel(models.Model):
    TYPE_CHOICES = (('lastest', '最新影片'), ('classis', '经典影片'))
    title = models.CharField(verbose_name="标题", max_length=128)
    release_time = models.DateTimeField(verbose_name="发布时间",null=True,blank=True)
    major_img_url = models.CharField(verbose_name="影片主图片", max_length=256,null=True,blank=True)
    moive_star_score = models.FloatField(verbose_name="评分",null=True,blank=True)
    moive_type = models.CharField(verbose_name="影片类型",max_length=64,null= True,blank=True)#比如科幻，悬疑，冒险等等
    summary_img_url = models.CharField(verbose_name="内容概要视频截图PIC", max_length=64, null=True, blank=True)
    content = models.TextField(verbose_name="影片介绍", max_length=1024, null=True, blank=True)
    ftp_url = models.CharField(verbose_name="ftp地址", max_length=64, null=True, blank=True)
    movie_classify = models.IntegerField(verbose_name="影片首页子类别",null=True,blank=True)#影片所属分类，是最新电影，首页推荐最新，首页迅雷资源等等
    movie_classify_child = models.CharField(verbose_name="影片类别",choices=TYPE_CHOICES,max_length=64,null=True,blank=True)#此字段只针对首页数据，因为首页数据可能有多个为最新推荐，经典推进等额定

    class Meta:
        db_table = 'movie_list'
        verbose_name = '影片列表'
        verbose_name_plural = '影片列表'

    def __unicode__(self):
        return self.title

# class MovieDetailModel(models.Model):
#     # TYPE_CHOICES = (('lastest', '最新影片'), ('classis', '经典影片'))
#     # title = models.CharField(verbose_name="标题",max_length=64,null=True,blank=True)
#     # release_time = models.DateTimeField(verbose_name="发布时间",null=True,blank=True)
#     # major_img_url = models.CharField(verbose_name="影片主图片",max_length=64,null=True,blank=True)
#     # moive_star_score = models.FloatField(verbose_name="评分",null=True,blank=True)
#     content = models.TextField(verbose_name="影片介绍",max_length=1024,null=True,blank=True)
#     summary_img_url = models.CharField(verbose_name="内容概要视频截图PIC",max_length=64,null=True,blank=True)
#     ftp_url = models.CharField(verbose_name="ftp地址",max_length=64,null=True,blank=True)
#     moive_detail = models.ForeignKey(MovieModel,verbose_name="所属的影片",null=True,blank=True)
#     movie_classify_child = models.CharField(verbose_name="影片类别", choices=TYPE_CHOICES, max_length=64, null=True,blank=True)  # 此字段只针对首页数据，因为首页数据可能有多个为最新推荐，经典推进等额定
#
#     class Meta:
#         db_table = "movie_detail"
#         verbose_name = "影片详情"
#         verbose_name_plural = "影片详情"
#
#     def __unicode__(self):
#         return self.title


# from django.contrib import admin
#admin.site.register(MovieDetailModel)