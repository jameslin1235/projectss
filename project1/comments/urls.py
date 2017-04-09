from django.conf.urls import url
from . import views

urlpatterns = [


    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/edit/$', views.comment_edit,name='comment_edit'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/delete/$', views.comment_delete, name='comment_delete'),


]
