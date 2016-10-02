#!/usr/bin/env python

from django.contrib import admin
from app.models import MovieDetailModel

class MovieDetailModel_Admin(admin.ModelAdmin):
    list_display = ('title','address','SOSPhone','contactPhone')

admin.site.register(MovieDetailModel,MovieDetailModel)

