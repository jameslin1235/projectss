from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^(?P<id>\d+)/edit/$', views.post_edit,name='post_edit'),
    url(r'^drafts/$', views.post_drafts,name='post_drafts'),
    url(r'^(?P<id>\d+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^(?P<id>\d+)/$', views.post_detail, name='post_detail'),
    # url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^like/$', views.post_like, name='post_like'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/likers/$', views.post_likers, name='post_likers'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/comments/$', views.post_comments, name='post_comments'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/commentscount/$', views.post_comments_count, name='post_comments_count'),
    url(r'^modal/$', views.post_create_modal, name='post_create_modal'),
]
