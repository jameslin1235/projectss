from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    # url(r'^404/$', views.post_404, name='post_404'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/edit/$', views.post_edit,name='post_edit'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.post_detail, name='post_detail'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/like/$', views.post_like, name='post_like'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/dislike/$', views.post_dislike, name='post_dislike'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/likers/$', views.post_likers, name='post_likers'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/bookmark/$', views.post_bookmark, name='post_bookmark'),
    url(r'^getloginmodal/$', views.get_login_modal, name='get_login_modal'),

]
