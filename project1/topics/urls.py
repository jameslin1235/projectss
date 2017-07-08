from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.to_topic_trending, name='to_topic_trending'),
    url(r'^trending/$', views.topic_trending, name='topic_trending'),
    # url(r'^recommended-for-you/$', views.topic_recommended, name='topic_recommended'),
    # url(r'^follow/$', views.topic_follow, name='topic_follow'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.topic_detail, name='topic_detail')
]
