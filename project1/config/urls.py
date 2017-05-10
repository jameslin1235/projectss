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
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static
from project1.project1.posts import views as home


urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', home.post_list, name='post_list'),
    url(r'^register/', include("project1.project1.accounts.urls", namespace="accounts") ),
    url(r'^admin/', admin.site.urls),
    url(r'^posts/', include("project1.project1.posts.urls", namespace="posts")),
    url(r'^comments/', include("project1.project1.comments.urls", namespace="comments")),
    url(r'^categories/', include("project1.project1.categories.urls", namespace="categories")),
    url(r'^profile/', include("project1.project1.profiles.urls", namespace="profiles")),
    url(r'^getloginmodal/$', home.get_login_modal, name='get_login_modal'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
