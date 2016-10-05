__author__ = 'zhangzebo'
from django.conf.urls import patterns, url
from rest_api.views import auth,movie,user
from views import auth

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^user/$', user),
    url(r'^auth/$',auth),
    url(r'^movie/$',movie),
)