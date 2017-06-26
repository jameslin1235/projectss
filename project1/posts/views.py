from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse,JsonResponse, QueryDict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from .models import Post, Like, Dislike
from .forms import PostForm
from project1.project1.comments.forms import CommentForm
from project1.project1.comments.models import Comment
from project1.project1.config import utility

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
    if request.method == "GET":
        form = PostForm()
        context = {}
        context['form'] = form
        context['title'] = "Create Post"
        return render(request,"post_create.html",context)
    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user.profile
            post.save()
            messages.success(request, "Draft created.")
            return redirect("profiles:profile_drafts", id=current_user.profile.id, slug=current_user.profile.slug)
        else:
            return JsonResponse(form.errors)

@login_required
def post_edit(request,id,slug):
    if request.method == "GET":
        post = get_object_or_404(Post, id=id)
        user = post.user
        current_user = request.user
        user_status = utility.get_user_status(user,current_user)
        if user_status == "self":
            context = {}
            if post.is_draft:
                context['title'] = "Edit Draft"
            else:
                context['title'] = "Edit Post"
            form = PostForm(instance=post)
            context['form'] = form
            template = "post_edit.html"
            return render(request,template,context)
        else:
            raise PermissionDenied
    elif request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            if post.is_draft:
                messages.success(request, "Draft edited.")
            else:
                messages.success(request, "Post edited.")
            return redirect(request.path)


@login_required
def post_delete(request,id,slug):
    if request.method == "GET":
        post = get_object_or_404(Post, id=id)
        user = post.user
        current_user = request.user
        user_status = utility.get_user_status(user,current_user)
        if user_status == "self":
            post.delete()
            if post.is_draft:
                messages.success(request, "Draft deleted.")
            else:
                messages.success(request, "Post deleted.")
            return redirect(request.path)
        else:
            raise PermissionDenied


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

def post_comments_count(request,id,slug):
    post = get_object_or_404(Post, id=id)
    if request.method == "GET" and request.is_ajax():
        if post.is_draft == True:
            raise PermissionDenied
        post_comments_count = post.get_comments_count()
        response_data = {}
        response_data['post_comments_count'] = post_comments_count
        return JsonResponse(response_data,safe=False)

def post_comments(request,id,slug):
    post = get_object_or_404(Post, id=id)
    user = post.user
    current_user = request.user
    if request.method == "GET" and request.is_ajax():
        if post.is_draft == True:
            raise PermissionDenied
        submit_button_text = "Comment"
        comments = post.get_comments()
        comments_count = post.get_comments_count()
        if comments_count == 0:
            no_comments = True
            current_page = 0
            is_pagination = 0
            page_num = 0
        else:
            no_comments = False
            args = [comments,10,request]
            current_page, is_pagination, page_num = functions.paginate(args)

        context = {
            "post":post,
            "submit_button_text":submit_button_text,
            "comments_count":comments_count,
            "no_comments":no_comments,
            "current_page":current_page,
            "is_pagination":is_pagination,
            "page_num":page_num,
        }

        template = "post_comments_collapse.html"
        if request.GET.get("template") and request.GET.get("template") == "template2":
            template = "post_comments_collapse_body.html"
        elif request.GET.get("template") and request.GET.get("template") == "template3":
            template = "post_comments_collapse_page.html"
        return render(request,template,context)


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
            # response_data['status'] = "unliked"
        else:
            # post.likes += 1
            Like.objects.create(post=post, profile=current_user.profile, date_liked=timezone.now())
            post.likes = post.likers.count()
            # response_data['status'] = "liked"

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



def post_likers(request,id,slug):
    post = get_object_or_404(Post, id=id)
    user = post.user
    current_user = request.user
    if request.method == "GET" and request.is_ajax():
        if post.is_draft == True:
            raise PermissionDenied
        users = [user,current_user]
        logged_in, user_status = get_user_status(users)


        no_likers = True
        if post.get_likers_count != 0:
            no_likers = False
        post_likers = post.get_likers()
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

            # person requests likers of a posts
            # if ano, follow
            # if self, check if you followed any of these people
            # if other, first check if among likers include you, if yes exclude yourself. Then check if you followed any of other people (leads to either follow or followed)
        follow_status = []
        for profile in current_page:
            if user_status == "anonymous":
                follow_status.append("Follow")
            elif user_status == "self":
                if current_user.profile.followed_user(profile):
                    follow_status.append("Followed")
                else:
                    follow_status.append("Follow")
            else:
                if current_user == profile.user:
                    follow_status.append("self")
                else:
                    if current_user.profile.followed_user(profile):
                        follow_status.append("Followed")
                    else:
                        follow_status.append("Follow")
        context = {
            "post":post,
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

        comments = post.get_comments()
        comments_count = post.get_comments_count()
        no_comments = True
        if comments_count != 0:
            no_comments = False
        comment_title = "Comments"
        submit_button_text = "Comment"
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
            "submit_button_text":submit_button_text,
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
