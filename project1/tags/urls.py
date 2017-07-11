from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.tag_detail, name='tag_detail')
]
