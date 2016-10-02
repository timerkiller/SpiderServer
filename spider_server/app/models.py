# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class MovieModel(models.Model):
    title = models.CharField(verbose_name="标题", max_length=64, null=True, blank=True)
    release_time = models.DateTimeField(verbose_name="发布时间", null=False, blank=False)
    major_img_url = models.CharField(verbose_name="影片主图片", max_length=64, null=True, blank=True)
    moive_star_score = models.IntegerField(verbose_name="评分",null=True, blank=True)

    class Meta:
        db_table = 'movie_list'
        verbose_name = '影片列表'
        verbose_name_plural = '影片列表'

    def __unicode__(self):
        return self.title

class MovieDetailModel(models.Model):
    title = models.CharField(verbose_name="标题",max_length=64,null=True,blank=True)
    release_time = models.DateTimeField(verbose_name="发布时间", null=False,blank=False)
    major_img_url = models.CharField(verbose_name="影片主图片",max_length=64,null=True,blank=True)
    moive_star_score = models.IntegerField(verbose_name="评分",max_length=64,null=True,blank=True)
    content = models.CharField(verbose_name="影片介绍",max_length=64,null=True,blank=True)
    summary_img_url = models.CharField(verbose_name="内容概要视频截图",max_length=64,null=True,blank=True)
    ftp_url = models.CharField(verbose_name="ftp地址",max_length=64,null=True,blank=True)
    moive_detail = models.ForeignKey(MovieModel,verbose_name="所属的影片",null=True,blank=True)

    class Meta:
        db_table = "movie_detail"
        verbose_name = "影片详情"
        verbose_name_plural = "影片详情"

        def __unicode__(self):
            return self.title




# from django.contrib import admin
#admin.site.register(MovieDetailModel)