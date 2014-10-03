from django.conf.urls import patterns, url

from words import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^(?P<word_id>\d+)/$', views.detail, name='detail'),
    url(r'^groups/$', views.wordgroup_index, name='wordgroup_index'),
    url(r'^groups/(?P<wordgroup_id>\d+)/$', views.wordgroup_detail, name='wordgroup_detail'),
    url(r'^groups/(?P<wordgroup_id>\d+)/(?P<word_id>\d+)/$', views.wordgroup_words, name='wordgroup_words'),
)