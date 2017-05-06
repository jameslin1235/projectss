from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse,JsonResponse, QueryDict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils import timezone

from django.core import serializers
from django.core.exceptions import PermissionDenied
from .models import Post, Like, Dislike
from .forms import PostForm
from project1.project1.comments.forms import CommentForm
from project1.project1.comments.models import Comment


# Create your views here.
def post_list(request):
    if request.method == "GET":
        current_user = request.user
        # anonymous user
        logged_in = False
        # logged-in user
        if current_user.is_authenticated:
            logged_in = True

        posts = Post.objects.filter(is_draft = False)
        posts_count = posts.count
        no_posts = True
        if posts_count != 0:
            no_posts = False
        title = "Latest Posts"
        comment_title = "Comments"
        comment_button_text = "Comment"
        form = CommentForm()
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

        no_comments = []
        comments_count = []
        comments_first_pages = []
        same_user = []
        for post in current_page.object_list:
            paginator = Paginator(post.comments.all(), 5) # Show 25 contacts per page
            try:
                comments_first_page = paginator.page(1)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                comments_first_page = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                comments_first_page = paginator.page(paginator.num_pages)
            comments_first_pages.append(comments_first_page)

            if post.comments.all().count() == 0:
                no_comments.append(True)
            else:
                no_comments.append(False)
            comments_count.append(post.comments.all().count())

            if current_user.is_authenticated:

                if post.user == current_user:
                    same_user.append(True)
                else:
                    same_user.append(False)

        context = {
            "current_user":current_user,
            "logged_in":logged_in,
            "no_posts":no_posts,
            "title":title,
            "comment_title":comment_title,
            "comment_button_text":comment_button_text,
            "form":form,
            "current_page":current_page,
            "comments_first_pages":comments_first_pages,
            "no_comments":no_comments,
            "comments_count":comments_count,
            "same_user":same_user,
        }

        return render(request,"post_list.html",context)



@login_required
def post_create(request):
    current_user = request.user
    if request.method == "GET":
            title = "Create Post"
            form = PostForm()
            context = {
                "title":title,
                "form":form,
            }
            return render(request,"post_create.html",context)
    elif request.method == "POST":
        if "save_draft" in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = current_user
                post.save()
                messages.success(request, "Draft created.")
                return redirect("profiles:profile_drafts", id=current_user.id, slug=current_user.profile.slug )
        elif "publish" in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = current_user
                post.is_draft = False
                post.date_published = timezone.now()
                post.save()
                messages.success(request, "Post created.")
                return redirect(post)



@login_required
def post_edit(request,id,slug):
    post = get_object_or_404(Post, id=id)
    if request.method == "GET":
        user = post.user
        current_user = request.user
        if current_user != user:
            raise PermissionDenied
        else:
            if post.is_draft == True:
                title = "Edit Draft"
                button_text = "Edit Draft"
            else:
                title = "Edit Post"
                button_text = "Edit Post"
            form = PostForm(instance=post)
            context = {
                "title":title,
                "button_text":button_text,
                "form":form,
            }
            if request.is_ajax():
                template = "post_edit_page.html"
            else:
                template = "post_edit.html"
            return render(request,template,context)

    elif request.method == "POST":
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            response_data = {}
            if post.is_draft == True:
                response_data['message'] = "Draft edited."
            else:
                response_data['message'] = "Post edited."
            return JsonResponse(response_data,safe=False)


@login_required
def post_delete(request,id,slug):
    post = get_object_or_404(Post, id=id)
    user = post.user
    current_user = request.user
    if request.method == "GET":
        if current_user != user:
            raise PermissionDenied
        post.delete()
        response_data = {}
        if post.is_draft == True:
            response_data['message'] = "Draft deleted."
        else:
            response_data['message'] = "Post deleted."
        return JsonResponse(response_data,safe=False)

@login_required
def post_publish(request,id,slug):
    post = get_object_or_404(Post, id=id)
    user = post.user
    current_user = request.user
    if request.method == "GET":
        if post.is_draft == False:
            raise PermissionDenied
        if current_user != user:
            raise PermissionDenied
        post.is_draft = False
        post.date_published = timezone.now()
        post.save()
        response_data = {}
        response_data['message'] = "Draft published."
        return JsonResponse(response_data,safe=False)


@login_required
def post_bookmark(request,id,slug):
    return render(request,"post_list.html",context)

@login_required
def post_like(request,id,slug):
    post = get_object_or_404(Post, id=id)
    user = post.user
    current_user = request.user
    if request.method == "GET":
        if post.is_draft == True:
            raise PermissionDenied
        if current_user == user:
            raise PermissionDenied
        response_data = {}
        if post.likers.filter(user=current_user).exists():
            # post.likes -= 1
            post.like_set.filter(profile=current_user.profile).delete()
            post.likes = post.likers.count()
            response_data['status'] = "unliked"
        else:
            # post.likes += 1
            Like.objects.create(post=post, profile=current_user.profile, date_liked=timezone.now())
            post.likes = post.likers.count()
            response_data['status'] = "liked"
        post.save()
        response_data['likes_count'] = post.likes
        return JsonResponse(response_data,safe=False)

@login_required
def post_dislike(request,id,slug):
    post = get_object_or_404(Post, id=id)
    user = post.user
    current_user = request.user
    if request.method == "GET":
        if post.is_draft == True:
            raise PermissionDenied
        if current_user == user:
            raise PermissionDenied
        response_data = {}
        if post.dislikers.filter(user=current_user).exists():
            # post.dislikes -= 1
            post.dislike_set.filter(profile=current_user.profile).delete()
            post.dislikes = post.dislikers.count()
            response_data['status'] = "undisliked"
        else:
            # post.dislikes += 1
            Dislike.objects.create(post=post, profile=current_user.profile, date_disliked=timezone.now())
            post.dislikes = post.dislikers.count()
            response_data['status'] = "disliked"
        post.save()
        response_data['dislikes_count'] = post.dislikes
        return JsonResponse(response_data,safe=False)

def get_login_modal(request):
    if request.method == "GET" and request.is_ajax():
        template = "login_modal.html"
        return render(request,template)

def post_likers(request,id,slug):
    post = get_object_or_404(Post, id=id)
    user = post.user
    current_user = request.user
    if request.method == "GET" and request.is_ajax():
        if post.is_draft == True:
            raise PermissionDenied

        # anonymous user
        follow_button_text = "Follow"
        logged_in = False
        user_status = "anonymous"

        # logged-in user
        if current_user.is_authenticated:
            logged_in = True
            if current_user == user:
                user_status = "self"
            else:
                user_status = "user"

        no_likers = True
        if post.likes != 0:
            no_likers = False
        post_likers = post.likers.all().order_by("like")
        paginator = Paginator(post_likers, 5) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            current_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            current_page = paginator.page(paginator.num_pages)
        next_page = 0
        is_more = False
        if current_page.has_next():
            next_page = current_page.next_page_number()
            is_more = True


        follow_status = []
        if user_status != "anonymous":
            for profile in current_page:
                if profile.user == current_user:
                    follow_status.append("Self")
                else:
                    if current_user.profile.following.filter(user=profile.user).exists():
                        follow_status.append("Followed")
                    else:
                        follow_status.append("Follow")

        context = {
            "post":post,
            "follow_button_text":follow_button_text,
            "logged_in":logged_in,
            "user_status":user_status,
            "no_likers":no_likers,
            "current_page":current_page,
            "next_page":next_page,
            "is_more":is_more,
            "follow_status":follow_status,
        }

        template = "post_likers_modal.html"
        if page is not None:
            template = "post_likers_modal_page.html"
        return render(request,template,context)


def post_detail(request,id,slug):
    post = get_object_or_404(Post, id=id)
    user = post.user
    current_user = request.user
    if request.method == "GET":
        if post.is_draft == True:
            raise PermissionDenied

        # anonymous user
        logged_in = False
        user_status = "anonymous"
        liked = False
        disliked = False

        # logged-in user
        if current_user.is_authenticated:
            logged_in = True
            if current_user == user:
                user_status = "self"
            else:
                user_status = "user"
                if post.likers.filter(user=current_user).exists():
                    liked = True
                if post.dislikers.filter(user=current_user).exists():
                    disliked = True

        comments = post.comments.all()
        comments_count = comments.count()
        no_comments = True
        if comments_count != 0:
            no_comments = False
        comment_title = "Comments"
        comment_button_text = "Comment"
        form = CommentForm()
        paginator = Paginator(comments, 5) # Show 25 contacts per page
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
            "post":post,
            "user":user,
            "current_user":current_user,
            "logged_in":logged_in,
            "user_status":user_status,
            "comments_count":comments_count,
            "no_comments":no_comments,
            "comment_title":comment_title,
            "comment_button_text":comment_button_text,
            "form":form,
            "current_page":current_page,
            "liked":liked,
            "disliked":disliked,
            }

        if request.is_ajax():
            template = "post_detail_page.html"
        else:
            template = "post_detail.html"
        return render(request,template,context)

    elif request.method == "POST" and request.is_ajax():
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.post = post
            comment.save()
            response_data = {}
            response_data['message'] = "Comment created."
            return JsonResponse(response_data,safe=False)
