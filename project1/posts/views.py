from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
from .forms import PostForm
from project1.project1.comments.forms import CommentForm
from project1.project1.comments.models import Comment
from django.http import JsonResponse
from django.core import serializers
# Create your views here.

def post_list(request):
    title = "Latest Posts"
    comment_title = "Comments"
    comment_button_text = "Comment"
    posts = Post.objects.filter(is_draft = False)
    logged_in = True
    if not request.user.is_authenticated:
        logged_in = False
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

    if request.method == "POST":
        form = CommentForm(request.POST)
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id = post_id)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment created.")
            return redirect("posts:post_list")
    else:
        form = CommentForm()
    context = {
        "title":title,
        "comment_title":comment_title,
        "comment_button_text":comment_button_text,
        "logged_in":logged_in,
        "current_page":current_page,
        "form":form,
    }

    return render(request,"post_list.html",context)

@login_required
def post_create(request):
    title = "Create Post"
    if request.method == "POST":
        if "save_draft" in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                messages.success(request, "Draft created.")
                return redirect("profiles:profile_drafts", id=request.user.id, slug=request.user.profile.slug )
        elif "publish" in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.is_draft = False
                post.date_published = timezone.now()
                post.save()
                messages.success(request, "Post created.")
                return redirect(post)
    else:
        form = PostForm()
    context = {
        "title":title,
        "form":form,
    }
    return render(request,"post_create.html",context)

@login_required
def post_edit(request,id,slug):
    post = get_object_or_404(Post, id=id)
    if post.is_draft == True:
        title = "Edit Draft"
        button_text = "Edit Draft"
    else:
        title = "Edit Post"
        button_text = "Edit Post"
    user = post.user
    current_user = request.user
    if current_user != user:
        return redirect("posts:post_404")
    else:
        if request.method == "POST":
            form = PostForm(request.POST,instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                if post.is_draft == True:
                    post.save()
                    messages.success(request, "Draft edited.")
                    return redirect("posts:post_edit", id=id, slug=slug )
                else:
                    post.save()
                    messages.success(request, "Post edited.")
                    return redirect(post)
        else:
            form = PostForm(instance=post)
    context = {
        "title":title,
        "button_text":button_text,
        "form":form,
    }
    return render(request,"post_edit.html",context)

@login_required
def post_delete(request,id,slug):
    post = get_object_or_404(Post, id=id)
    user = post.user
    current_user = request.user
    if current_user != user:
        return redirect("posts:post_404")
    else:
        if post.is_draft == True:
            post.delete()
            messages.success(request, "Draft deleted.")
            return redirect("profiles:profile_drafts", id=user.id, slug=user.profile.slug )
        else:
            post.delete()
            messages.success(request, 'Post deleted.')
            return redirect("profiles:profile_posts", id=user.id, slug=user.profile.slug )

def post_detail(request,id,slug):
    post = get_object_or_404(Post, id=id)
    if post.is_draft == True:
        return redirect("posts:post_404")
    user = post.user
    comments = Comment.objects.filter(post__id = id)
    comments_count = comments.count()
    no_comments = True
    if comments_count != 0:
        no_comments = False
    comment_title = "Comments"
    comment_button_text = "Comment"
    logged_in = True
    if not request.user.is_authenticated:
        logged_in = False



    if request.method == "POST":
        response_data = {}
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

            comments = Comment.objects.filter(post__id = id)
            paginator = Paginator(comments, 10) # Show 25 contacts per page
            page = request.GET.get('page')

            try:
                current_page = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                current_page = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                current_page = paginator.page(paginator.num_pages)

            response_data['avatar'] = comment.user.profile.avatar.url
            response_data['username'] = comment.user.username
            response_data['content'] = comment.content
            response_data['date_created'] = comment.date_created
            response_data['profile_url'] = reverse("profiles:profile_activity", kwargs={"id": comment.user.id, "slug":comment.user.profile.slug })
            response_data['count'] = comments_count + 1

            response_data['has_other_pages'] = current_page.has_other_pages()
            response_data['has_previous'] = current_page.has_previous()
            response_data['has_next'] = current_page.has_next()
            response_data['number'] = current_page.number
            response_data['page_range'] = current_page.paginator.page_range[-1]
            # messages.success(request, "Comment created.")
            return JsonResponse(response_data,safe=False)

    else:
        form = CommentForm()
        paginator = Paginator(comments, 10) # Show 25 contacts per page
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
        "user":user,
        "no_comments":no_comments,
        "comments_count":comments_count,
        "comment_title":comment_title,
        "comment_button_text":comment_button_text,
        "post":post,
        "logged_in":logged_in,
        "form":form,
    }

    return render(request,"post_detail.html",context)

@login_required
def post_publish(request,id,slug):
    post = get_object_or_404(Post, id=id)
    user = post.user
    current_user = request.user
    if current_user != user:
        return redirect("posts:post_404")
    else:
        if post.is_draft == False:
            return redirect("posts:post_404")
        else:
            post.is_draft = False
            post.date_published = timezone.now()
            post.save()
            messages.success(request, "Draft published.")
            return redirect("profiles:profile_drafts", id=user.id, slug=user.profile.slug )


def post_404(request):
    title = "404 page"
    context = {
        "title":title,
    }
    return render(request,"404.html",context)
