from django.contrib import admin
# Register your models here.

from app.models import MovieModel

# class MovieDetailModel_Admin(admin.ModelAdmin):
#     list_display = ('title','release_time','major_img_url','moive_star_score',)

class MovieModel_Admin(admin.ModelAdmin):
    list_display = ('title','release_time','major_img_url','moive_star_score','moive_type','movie_classify','summary_img_url','ftp_url')

# admin.site.register(MovieDetailModel,MovieDetailModel_Admin)
admin.site.register(MovieModel,MovieModel_Admin)