from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Topic, TopicUser
from project1.project1.posts.models import Post

# Create your views here.
# def topic_list(request):
#     if request.method == "GET":
#         context = {}
#         context['topics'] = Topic.objects.all()
#         return render(request,"topic_list.html",context)

def to_topic_trending(request):
    if request.method == "GET":
        return redirect("topics:topic_trending")

def topic_trending(request):
    if request.method == "GET":
        context = {}
        context['topics'] = Topic.objects.all()
        context['first_topics'] = Topic.objects.all()[:8]
        context['last_topics'] = Topic.objects.all()[8:14]
        return render(request,"topic_trending.html",context)


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
            if request.user.profile.first_login:
                id_list = request.GET.get("id").split(",")
                if id_list:
                    for x in id_list:
                        TopicUser.objects.create(user=request.user, topic=Topic.objects.get(id=int(x)), date_followed=timezone.now())
                request.user.profile.first_login = False
                request.user.profile.save()
                return redirect("home")
        else:
            raise PermissionDenied
