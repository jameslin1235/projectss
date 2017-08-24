from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.profile_detail, name='profile_detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.profile_edit,name='profile_edit'),
    url(r'^(?P<pk>\d+)/following/$', views.profile_following, name='profile_following'),
    url(r'^(?P<pk>\d+)/followers/$', views.profile_followers, name='profile_followers'),
    url(r'^(?P<pk>\d+)/posts/$', views.profile_posts, name='profile_posts'),
]
