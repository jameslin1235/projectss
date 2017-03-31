from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.category_list, name='category_list'),
    url(r'^(?P<slug>[-\w]+)/$', views.category_detail, name='category_detail'),

]
