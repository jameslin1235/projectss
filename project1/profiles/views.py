from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.http import JsonResponse
from project1.project1.posts.models import Post
from project1.project1.comments.models import Comment
from project1.project1.profiles.models import Profile
from project1.project1.posts.forms import PostForm
from project1.project1.comments.forms import CommentForm
from project1.project1.comments.models import Comment
from .forms import ProfileForm

# Create your views here.
def profile_activity(request,id,slug):
    title = "Activity"
    User = get_user_model()
    user = get_object_or_404(User, id = id)
    posts_count = user.post_set.filter(is_draft = False).count()
    drafts_count = user.post_set.filter(is_draft = True).count()
    context = {
        "title":title,
        "user":user,
        "posts_count":posts_count,
        "drafts_count":drafts_count,

    }

    return render(request,"profile_activity.html",context)

def profile_follow(request,id,slug):
    if request.method == "GET":
        User = get_user_model()
        user = get_object_or_404(User, id = id)
        current_user = request.user
        if current_user == user:
            raise PermissionDenied;
        else:
            #find if you already followed this guy
            if current_user.profile.objects.get(follows_)

            else:
                current_user.profile.follows.add(user.profile)
                response_data = {}
                response_data['message'] = "Draft edited."
                return JsonResponse(response_data,safe=False)
def profile_posts(request,id,slug):
    if request.method == "GET":
        User = get_user_model()
        user = get_object_or_404(User, id = id)
        logged_in = False
        if request.user.is_authenticated:
            logged_in = True
        current_user = request.user
        is_user = True
        if current_user != user:
            is_user = False
        posts = user.post_set.filter(is_draft = False).order_by("-date_created")
        option = 1

        if request.GET.get('option'):
            option = int(request.GET.get('option'))
            if option == 1:
                posts = user.post_set.filter(is_draft = False).order_by("-date_created")

            elif option == 2:
                posts = user.post_set.filter(is_draft = False).order_by("-date_edited")

            elif option == 3:
                posts = user.post_set.filter(is_draft = False).order_by("-date_published")

            elif option == 4:
                posts = user.post_set.filter(is_draft = False).order_by("-likes")

            elif option == 5:
                posts = user.post_set.filter(is_draft = False).order_by("-dislikes")

            elif option == 6:
                posts = user.post_set.filter(is_draft = False).annotate(num_comments=Count('comment')).order_by('-num_comments')


        posts_count = posts.count()
        drafts_count = user.post_set.filter(is_draft = True).count()
        no_posts = True
        if posts_count != 0:
            no_posts = False
        title = "Posts"
        comment_title = "Comments"
        comment_button_text = "Comment"
        paginator = Paginator(posts, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            current_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            current_page = paginator.page(paginator.num_pages)


        comments_count = []
        for post in current_page.object_list:
            comments_count.append(post.comment_set.all().count())
        form = CommentForm()
        current_url = request.path


        context = {
            "user":user,
            "logged_in":logged_in,
            "is_user":is_user,
            "posts_count":posts_count,
            "drafts_count":drafts_count,
            "no_posts":no_posts,
            "title":title,
            "comment_title":comment_title,
            "comment_button_text":comment_button_text,
            "current_page":current_page,
            "comments_count":comments_count,
            "form":form,
            "current_url":current_url,
            "option":option,
        }

        if request.is_ajax():
            template = "profile_posts_page.html"
        else:
            template = "profile_posts.html"

        return render(request,template,context)

# when you first come to page, you should be in first filter
#when you click on a different option, send a request to view to get template with filter

@login_required
def profile_drafts(request,id,slug):
    if request.method == "GET":
        User = get_user_model()
        user = get_object_or_404(User, id = id)
        current_user = request.user
        if current_user != user:
            raise PermissionDenied;
        else:
            is_user = True
            logged_in = False
            if request.user.is_authenticated:
                logged_in = True
            drafts = user.post_set.filter(is_draft = True).order_by("-date_created")
            option = 1

            if request.GET.get('option'):
                option = int(request.GET.get('option'))
                if option == 1:
                    drafts = user.post_set.filter(is_draft = True).order_by("-date_created")

                elif option == 2:
                    drafts = user.post_set.filter(is_draft = True).order_by("-date_edited")


            drafts_count = drafts.count()
            posts_count = user.post_set.filter(is_draft = False).count()
            no_drafts = True
            if drafts_count != 0:
                no_drafts = False
            title = "Drafts"
            paginator = Paginator(drafts, 10) # Show 25 contacts per page
            page = request.GET.get('page')
            try:
                current_page = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                current_page = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                current_page = paginator.page(paginator.num_pages)
            form = CommentForm()
            current_url = request.path

            context = {
                "user":user,
                "is_user":is_user,
                "logged_in":logged_in,
                "drafts_count":drafts_count,
                "posts_count":posts_count,
                "no_drafts":no_drafts,
                "title":title,
                "current_page":current_page,
                "form":form,
                "current_url":current_url,
                "option":option,
            }

            if request.is_ajax():
                template = "profile_drafts_page.html"
            else:
                template = "profile_drafts.html"

            return render(request,template,context)


def profile_comments(request,id,slug):
    title = "Comments"
    User = get_user_model()
    user = User.objects.get(id = id)
    current_user = request.user
    is_user = True
    if current_user != user:
        is_user = False
    comments = Comment.objects.filter(user__id = id)
    comments_count = comments.count()
    no_comments = True
    if comments_count != 0:
        no_comments = False

    paginator = Paginator(comments, 5) # Show 25 contacts per page
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
        "is_user":is_user,
        "comments_count":comments_count,
        "no_comments":no_comments,
        "current_page":current_page,
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

@login_required
def profile_edit(request,id,slug):
    title = "Edit Profile"
    button_text = "Edit Profile"
    User = get_user_model()
    user = User.objects.get(id = id)
    profile = user.profile
    current_user = request.user
    if current_user != user:
        return redirect("posts:post_404")
    else:
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES, instance = profile)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                messages.success(request, 'Profile edited.')
                return redirect('profiles:profile_edit', id=user.id, slug=user.profile.slug )
        else:
            form = ProfileForm(instance = profile)
    context = {
        "title":title,
        "button_text":button_text,
        "form":form,
    }
    return render(request,"profile_edit.html",context)
