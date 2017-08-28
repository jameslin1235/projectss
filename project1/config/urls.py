"""project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from project1.project1.users import views as users

urlpatterns = [
    url(r'^$', users.home, name="home"),
    url(r'^admin/', admin.site.urls),
    # url(r'^drafts/$', profiles.profile_drafts, name='profile_drafts'),
    url(r'^posts/', include("project1.project1.posts.urls", namespace="posts")),
    url(r'^tags/', include("project1.project1.tags.urls", namespace="tags")),
    url(r'^users/', include("project1.project1.users.urls", namespace="users")),
    url(r'^sessions/', include("project1.project1.session.urls", namespace="sessions")),
    url(r'^tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
