from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.post_list, name='post_list'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/update/$', views.post_update,name='post_update'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.post_detail, name='post_detail'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/publish/$', views.post_publish, name='post_publish'),

]
