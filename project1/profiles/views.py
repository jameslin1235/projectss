from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.utils import timezone
from project1.project1.posts.models import Post
from django.contrib.auth.models import User
from project1.project1.comments.models import Comment
from .models import Profile, Follow
from project1.project1.posts.forms import PostForm
from project1.project1.comments.forms import CommentForm
from .forms import ProfileForm, ProfileAvatarForm
from project1.project1.config import utility
from PIL import Image
import base64
import os

# Create your views here.
def profile_activity(request,id,slug):
    if request.method == "GET":
        user = get_object_or_404(get_user_model(), id = id)
        current_user = request.user
        context = {}
        user_status = utility.get_user_status(user,current_user)
        context['user_status'] = user_status
        if user_status != "self":
            context['user_follow_status'] = utility.get_user_follow_status(user,current_user,user_status)
        context['user_profile_status'] = user.profile.get_profile_status()
        if not user.profile.get_profile_status():
            context['user_profile_fields'] = user.profile.get_profile_fields()
        context['user'] = user
        context['title'] = "Activity"
        context['posts_count'] = user.profile.get_posts_count()
        context['drafts_count'] = user.profile.get_drafts_count()
        template = "profile_activity.html"
        return render(request,template,context)


def profile_drafts(request,id,slug):
    if request.method == "GET":
        user = get_object_or_404(get_user_model(), id = id)
        current_user = request.user
        context = {}
        user_status = utility.get_user_status(user,current_user)
        if user_status == "self":
            context['user_status'] = user_status
            if user_status != "self":
                context['user_follow_status'] = utility.get_user_follow_status(user,current_user,user_status)
            context['user_profile_status'] = user.profile.get_profile_status()
            if not user.profile.get_profile_status():
                context['user_profile_fields'] = user.profile.get_profile_fields()
            context['user'] = user
            context['posts_count'] = user.profile.get_posts_count()
            context['drafts_count'] = user.profile.get_drafts_count()
            if user.profile.get_drafts_count() != 0:
                context['drafts'] = user.profile.get_drafts()
                paginator = Paginator(user.profile.get_drafts(), 10) # Show 25 contacts per page
                page = request.GET.get('page')
                try:
                    current_page = paginator.page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    current_page = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    current_page = paginator.page(paginator.num_pages)
                context['current_page'] = current_page
            template = "profile_drafts.html"
            return render(request,template,context)
        else:
            raise PermissionDenied

def profile_posts(request,id,slug):
    if request.method == "GET":
        user = get_object_or_404(get_user_model(), id = id)
        current_user = request.user
        context = {}
        user_status = utility.get_user_status(user,current_user)
        context['user_status'] = user_status
        if user_status != "self":
            context['user_follow_status'] = utility.get_user_follow_status(user,current_user,user_status)
        context['user_profile_status'] = user.profile.get_profile_status()
        if not user.profile.get_profile_status():
            context['user_profile_fields'] = user.profile.get_profile_fields()
        context['user'] = user
        context['drafts_count'] = user.profile.get_drafts_count()
        context['posts_count'] = user.profile.get_posts_count()
        if user.profile.get_posts_count() != 0:
            context['posts'] = user.profile.get_posts()
            paginator = Paginator(user.profile.get_posts(), 10) # Show 25 contacts per page
            page = request.GET.get('page')
            try:
                current_page = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                current_page = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                current_page = paginator.page(paginator.num_pages)
            context['current_page'] = current_page
        template = "profile_posts.html"
        return render(request,template,context)

@login_required
def profile_edit(request):
    if request.method == "GET":
        current_user = request.user
        context = {}
        profile = current_user.profile
        context['form'] = ProfileForm(instance = profile)
        context['profile_avatar_form'] = ProfileAvatarForm(instance = profile)
        context['user'] = current_user
        return render(request,"profile_edit.html",context)
    elif request.method == "POST":
        form = ProfileForm(request.POST,instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile edited.")
            return redirect(request.path)
        else:
            context = {}
            context['form'] = form
            return render(request,"profile_edit.html",context)


def profile_edit_avatar(request):
    if request.method == "POST" and request.is_ajax():
        dataurl = request.POST['dataurl']
        filename = request.POST['filename']
        if request.user.profile.avatar.name != "default/avatar.jpg":
            request.user.profile.avatar.delete(save=False)
        decoded = base64.b64decode(dataurl)
        path = os.path.join(settings.MEDIA_ROOT, "users/%s/%s" % (request.user.username,filename))
        with open(path, "wb") as f:
            f.write(decoded)
        request.user.profile.avatar = "users/%s/%s" % (request.user.username,filename)
        request.user.profile.save()
        response = {}
        response['profile_avatar_url'] = request.user.profile.avatar.url
        return JsonResponse(response)

def profile_edit_background(request):
    if request.method == "POST" and request.is_ajax():
        dataurl = request.POST['dataurl']
        filename = request.POST['filename']
        if request.user.profile.background.name != "default/background.jpg":
            request.user.profile.background.delete(save=False)
        decoded = base64.b64decode(dataurl)
        path = os.path.join(settings.MEDIA_ROOT, "users\%s\%s" % (request.user.username,filename))
        with open(path, "wb") as f:
            f.write(decoded)
        request.user.profile.background = "users\%s\%s" % (request.user.username,filename)
        request.user.profile.save()
        response = {}
        response['profile_background_url'] = request.user.profile.background.url
        return JsonResponse(response)




def demo(request):
        return render(request,"demo.html")



@login_required
def profile_follow(request,id,slug):
    if request.method == "GET" and request.is_ajax():
        User = get_user_model()
        user = get_object_or_404(User, id = id)
        current_user = request.user

        # logged-in user
        if current_user.is_authenticated:
            if current_user == user:
                raise PermissionDenied;
            else:
                response_data = {}
                if request.GET.get("follow_status"):
                    follow_status = request.GET.get("follow_status")
                    if follow_status == "Follow":
                        current_user.profile.follow_user(user.profile)
                        response_data['follow_status'] = "Followed"
                        #follow this Person
                    elif follow_status == "Followed" or follow_status == "Unfollow":
                        current_user.profile.unfollow_user(user.profile)
                        response_data['follow_status'] = "Follow"
                        #unfollow
                return JsonResponse(response_data,safe=False)



def profile_following_count(request,id,slug):
    if request.method == "GET" and request.is_ajax():
        profile = get_object_or_404(Profile, id = id)
        profile_following_count = profile.get_following_count()
        response_data = {}
        response_data['profile_following_count'] = profile_following_count
        return JsonResponse(response_data,safe=False)

def profile_followers_count(request,id,slug):
    if request.method == "GET" and request.is_ajax():
        profile = get_object_or_404(Profile, id = id)
        profile_followers_count = profile.get_followers_count()
        response_data = {}
        response_data['profile_followers_count'] = profile_followers_count
        return JsonResponse(response_data,safe=False)




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
    if request.method == "GET":
        User = get_user_model()
        user = get_object_or_404(User, id=id)
        current_user = request.user

        # anonymous user
        logged_in = False
        user_status = "anonymous"

        # logged-in user
        if current_user.is_authenticated:
            logged_in = True
            if current_user == user:
                user_status = "self"
            else:
                user_status = "user"

        user_profile_url = user.profile.get_absolute_url()
        current_url = request.path
        following = user.profile.following.order_by('dest')  # sort following by latest
        following_count = following.count()
        posts_count = user.posts.filter(is_draft = False).count()
        drafts_count = user.posts.filter(is_draft = True).count()
        followers_count = user.profile.get_followers_count()
        no_following = True
        if following_count != 0:
            no_following = False
        title = "Following"
        paginator = Paginator(following, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            current_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            current_page = paginator.page(paginator.num_pages)


        user_follow_status = "Follow"
        user_message_status = "Message"
        if user_status == "self":
            user_follow_status = "self"
            user_message_status = "self"
        elif user_status == "user":
            if current_user.profile.following.filter(user=user).exists():
                user_follow_status = "Followed"
            else:
                user_follow_status = "Follow"
            user_message_status = "Message"

        follow_status = []
        for profile in current_page:
            if user_status == "anonymous":
                follow_status.append("Follow")
            elif user_status == "self":
                follow_status.append("Followed")
            else:
                if current_user == profile.user:
                    follow_status.append("")
                else:
                    if current_user.profile.following.filter(user=profile.user).exists():
                        follow_status.append("Followed")
                    else:
                        follow_status.append("Follow")

        context = {
            "user":user,
            "current_user":current_user,
            "logged_in":logged_in,
            "user_status":user_status,
            "user_profile_url":user_profile_url,
            "following_count":following_count,
            "drafts_count":drafts_count,
            "posts_count":posts_count,
            "followers_count":followers_count,
            "no_following":no_following,
            "title":title,
            "current_page":current_page,
            "user_follow_status":user_follow_status,
            "user_message_status":user_message_status,
            "follow_status":follow_status,

        }

        if request.is_ajax():
            template = "profile_following_page.html"
        else:
            template = "profile_following.html"

        return render(request,template,context)

def profile_followers(request,id,slug):
    if request.method == "GET":
        User = get_user_model()
        user = get_object_or_404(User, id=id)
        current_user = request.user

        # anonymous user
        logged_in = False
        user_status = "anonymous"

        # logged-in user
        if current_user.is_authenticated:
            logged_in = True
            if current_user == user:
                user_status = "self"
            else:
                user_status = "user"
        # # logged-in user
        # if current_user.is_authenticated:
        #     logged_in = True
        #     if current_user == user:
        #         is_user = True
        #     else:
        #         is_user = False
        #         if current_user.profile.following.filter(user=user).exists():
        #             top_follow_button_text = "Followed"

        user_profile_url = user.profile.get_absolute_url()
        current_url = request.path
        followers = user.profile.followers.order_by('source')

        # followers = Profile.objects.filter(following=user.profile).order_by('source')
        followers_count = followers.count()
        posts_count = user.posts.filter(is_draft = False).count()
        drafts_count = user.posts.filter(is_draft = True).count()
        following_count = user.profile.get_following_count()
        no_followers = True
        if followers_count != 0:
            no_followers = False
        title = "Followers"
        paginator = Paginator(followers, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            current_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            current_page = paginator.page(paginator.num_pages)


        user_follow_status = "Follow"
        user_message_status = "Message"
        if user_status == "self":
            user_follow_status = "self"
            user_message_status = "self"
        elif user_status == "user":
            if current_user.profile.following.filter(user=user).exists():
                user_follow_status = "Followed"
            else:
                user_follow_status = "Follow"
            user_message_status = "Message"

        follow_status = []
        for profile in current_page:
            if user_status == "anonymous":
                follow_status.append("Follow")
            elif user_status == "self":
                if current_user.profile.following.filter(user=profile.user).exists():
                    follow_status.append("Followed")
                else:
                    follow_status.append("Follow")
            else:
                if current_user == profile.user:
                    follow_status.append("")
                else:
                    if current_user.profile.following.filter(user=profile.user).exists():
                        follow_status.append("Followed")
                    else:
                        follow_status.append("Follow")


        context = {
            "user":user,
            "current_user":current_user,

            "logged_in":logged_in,
            "user_status":user_status,
            "user_profile_url":user_profile_url,
            "followers_count":followers_count,

            "drafts_count":drafts_count,
            "posts_count":posts_count,
            "following_count":following_count,
            "no_followers":no_followers,
            "title":title,
            "current_page":current_page,
            "user_follow_status":user_follow_status,
            "user_message_status":user_message_status,
            "follow_status":follow_status,
        }

        if request.is_ajax():
            template = "profile_followers_page.html"
        else:
            template = "profile_followers.html"

        return render(request,template,context)
