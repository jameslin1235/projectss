from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.profile_activity, name='profile_activity'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/posts/$', views.profile_posts, name='profile_posts'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/drafts/$', views.profile_drafts, name='profile_drafts'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/comments/$', views.profile_comments, name='profile_comments'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/bookmarks/$', views.profile_bookmarks, name='profile_bookmarks'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/following/$', views.profile_following, name='profile_following'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/followers/$', views.profile_followers, name='profile_followers'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/follow/$', views.profile_follow, name='profile_follow'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/followingcount/$', views.profile_following_count, name='profile_following_count'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/followerscount/$', views.profile_followers_count, name='profile_followers_count'),

    url(r'^edit/$', views.profile_edit, name='profile_edit'),
    url(r'^editavatar/$', views.profile_edit_avatar, name='profile_edit_avatar'),
    url(r'^editbackground/$', views.profile_edit_background, name='profile_edit_background'),


    url(r'^demo/$', views.demo, name='demo'),
]
