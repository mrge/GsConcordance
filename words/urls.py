from django.conf.urls import patterns, url

from words import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^(?P<word_id>\d+)/$', views.detail, name='detail'),
    url(r'^groups/$', views.wordgroup_index, name='wordgroup_index'),
    url(r'^groups/(?P<wordgroup_id>\d+)/$', views.wordgroup_detail, name='wordgroup_detail'),
    url(r'^groups/(?P<wordgroup_id>\d+)/(?P<word_id>\d+)/$', views.wordgroup_words, name='wordgroup_words'),
    url(r'^phrases/$', views.wordphrase_index, name='wordphrase_index'),
    url(r'^phrases/(?P<wordphrase_id>\d+)/$', views.wordphrasefilewordall_detail, name='wordphrasefilewordall_detail'),
    url(r'^phrases/(?P<wordphrase_id>\d+)/(?P<file_id>\d+)/$', views.wordphrasefileword_detail, name='wordphrasefileword_detail'),
    
)