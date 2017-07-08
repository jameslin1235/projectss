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
from project1.project1.config import utility
from project1.project1.posts import views as posts
from project1.project1.accounts import views as accounts

urlpatterns = [

    url(r'^$', posts.home, name="home"),
    url(r'^signup/', accounts.signup_view, name="signup"),
    url(r'^login/', accounts.login_view, name="login"),
    url(r'^logout/', accounts.logout_view, name="logout"),
    url(r'^admin/', admin.site.urls),
    url(r'^posts/', include("project1.project1.posts.urls", namespace="posts")),
    url(r'^explore/', include("project1.project1.topics.urls", namespace="topics")),
    url(r'^profile/', include("project1.project1.profiles.urls", namespace="profiles")),
    url(r'^getloginmodal/$', utility.get_login_modal, name='get_login_modal'),
    url(r'^getalert/$', utility.get_alert, name='get_alert'),
    url(r'^geterror/$', utility.get_error, name='get_error'),
    url(r'^getloader/$', utility.get_loader, name='get_loader'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
