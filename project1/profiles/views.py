from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from project1.project1.posts.models import Post
from project1.project1.posts.forms import PostForm
# Create your views here.

@login_required
def profile_activity(request,id,slug):

    title = "Activity"
    context = {
        "title":title,
    }

    return render(request,"profile_activity.html",context)

@login_required
def profile_posts(request,id,slug):
    title = "Posts"
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
        "title":title,
        "current_page":current_page,
        "posts_count":posts_count,
        "no_posts":no_posts,
    }

    return render(request,"profile_posts.html",context)

@login_required
def profile_comments(request,id,slug):

    title = "Comments"
    context = {
        "title":title,
    }

    return render(request,"profile_comments.html",context)

@login_required
def profile_bookmarks(request,id,slug):

    title = "Bookmarks"
    context = {
        "title":title,
    }

    return render(request,"profile_bookmarks.html",context)

@login_required
def profile_following(request,id,slug):

    title = "Following"
    context = {
        "title":title,
    }

    return render(request,"profile_following.html",context)

@login_required
def profile_followers(request,id,slug):

    title = "Followers"
    context = {
        "title":title,
    }

    return render(request,"profile_followers.html",context)
