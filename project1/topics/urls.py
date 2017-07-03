from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.topic_list, name='topic_list'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.topic_detail, name='topic_detail')
]
