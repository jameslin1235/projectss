from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import Topic
from project1.project1.posts.models import Post

# Create your views here.

#
# def category_list(request):
#     categories = Category.objects.all()
#     title = "Categories"
#     context = {
#         "categories":categories,
#         "title":title,
#     }
#     return render(request,"category_list.html",context)


def topic_detail(request,id,slug):
    if request.method == "GET":
        topic = get_object_or_404(Topic, id=id)
        context = {}
        context['topic_posts'] = topic.get_posts()
        return render(request,"topic_detail.html",context)
