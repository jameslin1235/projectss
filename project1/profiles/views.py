from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from project1.project1.posts.models import Post
from project1.project1.posts.forms import PostForm
# Create your views here.

@login_required
def profile_list(request,id,slug):

    # posts = Post.objects.filter(user__id = id)
    # posts_count = posts.count()
    # no_posts = True
    # if posts_count != 0:
    #     no_posts = False
    #
    # paginator = Paginator(posts, 5) # Show 25 contacts per page
    # page = request.GET.get('page')
    # try:
    #     current_page = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     current_page = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     current_page = paginator.page(paginator.num_pages)
    #
    # context = {
    #     "current_page":current_page,
    #     "posts_count":posts_count,
    #     "no_posts":no_posts,
    # }

    return render(request,"profile_list.html")

def profile_posts(request,id,slug):
    posts = Post.objects.filter(user__id = id)
    posts_count = posts.count()
    no_posts = True
    if posts_count != 0:
        no_posts = False

    paginator = Paginator(posts, 5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        current_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        current_page = paginator.page(paginator.num_pages)

    context = {
        "current_page":current_page,
        "posts_count":posts_count,
        "no_posts":no_posts,
    }

    return render(request,"profile_list.html",context)


def profile_activity(request,id,slug):

    return render(request,"profile_list.html")


def profile_comments(request,id,slug):

    return render(request,"profile_list.html")


def profile_bookmarks(request,id,slug):

    return render(request,"profile_list.html")


def profile_following(request,id,slug):

    return render(request,"profile_list.html")


def profile_followers(request,id,slug):

    return render(request,"profile_list.html")
