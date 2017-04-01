from django.conf.urls import url
from . import views

urlpatterns = [

    # url(r'^$', views.profile_list, name='profile_list'),
    # url(r'^create/$', views.post_create, name='post_create'),
    # url(r'^(?P<id>\d+)/update/$', views.post_update,name='post_update'),
    # url(r'^(?P<id>\d+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^(?P<slug>[-\w]+)/$', views.profile_list, name='profile_list'),
]
