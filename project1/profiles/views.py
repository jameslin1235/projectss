from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from project1.project1.posts.models import Post
from project1.project1.posts.forms import PostForm
from .forms import ProfileForm

# Create your views here.
def profile_activity(request,id,slug):
    title = "Activity"
    User = get_user_model()
    user = User.objects.get(id = id)
    context = {
        "title":title,
        "user":user,
    }

    return render(request,"profile_activity.html",context)


def profile_posts(request,id,slug):
    title = "Posts"
    User = get_user_model()
    user = User.objects.get(id = id)
    posts = Post.objects.filter(user__id = id, is_draft = False)
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
        "user":user,
        "posts_count":posts_count,
        "no_posts":no_posts,
        "current_page":current_page,
    }

    return render(request,"profile_posts.html",context)



def profile_drafts(request,id,slug):
    title = "Drafts"
    User = get_user_model()
    user = User.objects.get(id = id)
    drafts = Post.objects.filter(user__id = id, is_draft = True)
    drafts_count = drafts.count()
    no_drafts = True
    if drafts_count != 0:
        no_drafts = False

    paginator = Paginator(drafts, 5) # Show 25 contacts per page
    page = request.GET.get("page")
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
        "user":user,
        "drafts_count":drafts_count,
        "no_drafts":no_drafts,
        "current_page":current_page,
    }

    return render(request,"profile_drafts.html",context)

def profile_comments(request,id,slug):
    title = "Comments"
    User = get_user_model()
    user = User.objects.get(id = id)
    context = {
        "title":title,
        "user":user,
    }

    return render(request,"profile_comments.html",context)

def profile_bookmarks(request,id,slug):
    title = "Bookmarks"
    User = get_user_model()
    user = User.objects.get(id = id)
    context = {
        "title":title,
        "user":user,
    }

    return render(request,"profile_bookmarks.html",context)


def profile_following(request,id,slug):

    title = "Following"
    User = get_user_model()
    user = User.objects.get(id = id)
    context = {
        "title":title,
        "user":user,
    }

    return render(request,"profile_following.html",context)


def profile_followers(request,id,slug):

    title = "Followers"
    User = get_user_model()
    user = User.objects.get(id = id)
    context = {
        "title":title,
        "user":user,
    }

    return render(request,"profile_followers.html",context)

def profile_edit(request):

    title = "edit profile"
    if request.method == "POST":
        if "publish" in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.is_draft = False
                post.save()
                messages.success(request, 'Post created.')
                return redirect(post)
        elif "save_draft" in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                messages.success(request, 'Draft created.')
                return redirect('profiles:profile_drafts', id=request.user.id, slug=request.user.profile.slug )

        else:
            form = ProfileForm()




    context = {
        "title":title,
        "form":form,
    }

    return render(request,"profile_edit.html",context)
