from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.post_list),
    url(r'^create/$', views.post_create),
    url(r'^update/$', views.post_update),
    url(r'^delete/$', views.post_delete),
    url(r'^(?P<id>\d+)/$', views.post_detail, name='post_detail'),
]
