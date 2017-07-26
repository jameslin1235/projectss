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
from .models import Post, PostUser
from project1.project1.tags.models import Tag
from .forms import PostForm
from project1.project1.accounts.forms import UserForm, LoginForm
from project1.project1.config import utility
from project1.project1.posts.forms import PostForm

# Create your views here.
def post_create_modal(request):
    if request.method == "GET" and request.is_ajax():
        context = {}
        context['form'] = PostForm()
        template = "post_create_modal.html"
        return render(request,template,context)
    else:
        raise PermissionDenied

def post_detail(request,id,slug):
    if request.method == "GET":
        post = get_object_or_404(Post, id=id)
        if post.is_draft:
            raise PermissionDenied
        else:
            context = {}
            context['post'] = post
            context['user'] = post.user
            if request.user.is_authenticated and request.user != post.user:
                context['liked_post'] = request.user.profile.liked_post(post)
            return render(request,"post_detail.html",context)

def home(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            if request.user.profile.first_login: # see first-time login topic follow page
                context = {}
                context['general_tags'] = Tag.objects.filter(general = True)
                return render(request,"tag_follow.html",context)
            else: # view personalized home
                context = {}
                if request.user.followed_tags.count() == 0: # view main tags
                    context['main_tags'] = Tag.objects.filter(main = True)
                    return render(request,"home.html",context)
                else:
                    context['main_tags'] = Tag.objects.filter(main = True)
                    context['tags'] = request.user.followed_tags.all() # display followed tags
                    return render(request,"dashboard.html",context)
        else: # view main tags
            context = {}
            context['main_tags'] = Tag.objects.filter(main = True)
            return render(request,"home.html",context)

@login_required
def post_create(request):
    if request.method == "GET":
        form = PostForm()
        context = {}
        context['form'] = form
        return render(request,"post_create.html",context)
    elif request.method == "POST" and request.is_ajax():
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if not post.title:
                post.title = "Untitled"
            post.user = request.user
            post.save()
            response = {}
            response['url'] = post.get_edit_url()
            return JsonResponse(response)
        else:
            print('w')

@login_required
def post_edit(request,id):
    if request.method == "GET":
        print('w')
    elif request.method == "POST" and request.is_ajax():
        post = Post.objects.get(id = id)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            response = {}
            return JsonResponse(response)

@login_required
def post_drafts(request):
    if request.method == "GET":
        context = {}
        # context['drafts'] = request.user.profile.get_drafts()
        context['drafts_count'] = request.user.profile.get_drafts_count()
        paginator = Paginator(request.user.profile.get_drafts(), 25) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            drafts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            drafts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            drafts = paginator.page(paginator.num_pages)
        context['drafts'] = drafts
        return render(request,"post_drafts.html",context)

    #     # if request.POST.get('field') == "title":
    #
    #     #     print(Post.objects.create(user=request.user, title=request.POST.get('value')))
    #     #
    #     # else:
    #     #     Post.objects.create(user=request.user, content=request.POST.get('value'))
    #
    #
    #
    #
    # # elif request.method == "POST":
    # #     if request.GET.get("action") == "Post":
    # #         form = PostForm(request.POST)
    # #         if form.is_valid():
    # #             post = form.save(commit=False)
    # #             post.user = request.user
    # #             post.date_published = timezone.now()
    # #             post.is_draft = False
    # #             post.save()
    # #             messages.success(request, "Post created.")
    # #             return redirect("home")
    # #         else:
    # #             print('wrong')
    # #     else:
    # #         form = PostForm(request.POST)
    # #         if form.is_valid():
    # #             post = form.save(commit=False)
    # #             post.user = request.user
    # #             post.is_draft = True
    # #             post.save()
    # #             messages.success(request, "Draft created.")
    # #             return redirect("home")
    # #         else:
    # #             print('wrong')
    #
    #
    #
    # if request.method == "GET":
    #     post = get_object_or_404(Post, id=id)
    #     user = post.user
    #     if request.user == user:
    #         context = {}
    #         if post.is_draft:
    #             context['title'] = "Edit Draft"
    #         else:
    #             context['title'] = "Edit Post"
    #         form = PostForm(instance=post)
    #         context['form'] = form
    #         template = "post_edit.html"
    #         return render(request,template,context)
    #     else:
    #         raise PermissionDenied
    # elif request.method == "POST":
    #     post = Post.objects.get(id = id)
    #     form = PostForm(request.POST, instance=post)
    #     if form.is_valid():
    #         form.save()
    #         if post.is_draft:
    #             messages.success(request, "Draft edited.")
    #         else:
    #             messages.success(request, "Post edited.")
    #         return redirect(request.path)

@login_required
def post_delete(request,id,slug):
    if request.method == "GET":
        post = get_object_or_404(Post, id=id)
        user = post.user
        if request.user == user:
            post.delete()
            if post.is_draft:
                messages.success(request, "Draft deleted.")
                return redirect("profiles:profile_drafts")
            else:
                messages.success(request, "Post deleted.")
                return redirect("profiles:profile_posts", id=request.user.id, slug=request.user.profile.slug)
        else:
            raise PermissionDenied

# @login_required
# def post_publish(request,id,slug):
#     if request.method == "GET":
#         post = get_object_or_404(Post, id=id)
#         user = post.user
#         if request.user == user:
#             if post.is_draft:
#                 post.is_draft = False
#                 post.date_published = timezone.now()
#                 post.save()
#                 messages.success(request, "Draft published.")
#                 return redirect("profiles:profile_posts", id=request.user.id, slug=request.user.profile.slug)
#             else:
#                 raise PermissionDenied
#         else:
#             raise PermissionDenied
#
#

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
def post_like(request):
    if request.method == "GET" and request.is_ajax():
        id = request.GET.get("id")
        liked = request.GET.get("liked")
        post = Post.objects.get(id=id)
        if liked == "liked":
            post.likes -= 1
            Like.objects.filter(post=post, user=request.user).delete()
        else:
            post.likes += 1
            Like.objects.create(post=post, user=request.user, date_liked=timezone.now())
        post.save()
        response = {}
        response['likes'] = post.likes
        return JsonResponse(response)
    else:
        raise PermissionDenied

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
