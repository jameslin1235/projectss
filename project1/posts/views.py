from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
from .forms import PostForm
from project1.project1.comments.forms import CommentForm
# Create your views here.

def post_list(request):
    title = "Latest Posts"
    posts = Post.objects.filter(is_draft = False)
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
    comment_title = "Comment"
    comment_button_text = "Comment"
    post = get_object_or_404(Post, id=id)
    if post.is_draft == True:
        return redirect("posts:post_404")
    not_logged_in = False
    if not request.user.is_authenticated:
        not_logged_in = True
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment created.")
            return redirect(post)
    else:
        form = CommentForm()

    context = {
        "comment_title":comment_title,
        "comment_button_text":comment_button_text,
        "post":post,
        "not_logged_in":not_logged_in,
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
        post.is_draft = False
        post.date_published = timezone.now()
        post.save()
        messages.success(request, "Draft published.")
        return redirect("profiles:profile_drafts", id=user.id, slug=user.profile.slug )

@login_required
def post_404(request):
    title = "404 page"
    context = {
        "title":title,
    }
    return render(request,"404.html",context)
