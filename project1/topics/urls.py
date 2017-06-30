from django.conf.urls import url
from . import views

urlpatterns = [

    # url(r'^$', views.category_list, name='category_list'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.topic_detail, name='topic_detail'),


]
