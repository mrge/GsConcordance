from django.conf.urls import patterns, url

from files import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^(?P<file_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<file_id>\d+)/(?P<word_id>\d+)/$', views.fileword_detail, name='fileword_detail'),
)