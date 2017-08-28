from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.session_list, name='session_list'),
    url(r'^new/$', views.session_create, name='session_create'),
]
