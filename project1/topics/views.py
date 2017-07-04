from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import Topic
from project1.project1.posts.models import Post

# Create your views here.
def topic_list(request):
    if request.method == "GET":
        context = {}
        context['topics'] = Topic.objects.all()
        return render(request,"topic_list.html",context)

def topic_detail(request,id,slug):
    if request.method == "GET":
        topic = get_object_or_404(Topic, id=id)
        context = {}
        context['topic'] = topic
        context['topic_posts'] = topic.get_posts()
        if request.user.is_authenticated:
            value = []
            for post in topic.get_posts():
                if request.user == post.user:
                    value.append("self")
                else:
                    if request.user.profile.liked_post(post):
                        value.append(True)
                    else:
                        value.append(False)
            context['value'] = value
        else:
            context['anonymous'] = True
        return render(request,"topic_detail.html",context)

def topic_follow(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            context = {}
            context['topics'] = Topic.objects.all()
            return render(request,"topic_follow.html",context)
        else:
            raise PermissionDenied
