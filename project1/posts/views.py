from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
from .forms import PostForm
# Create your views here.


def post_list(request):
    posts = Post.objects.all()
    title = "Latest Posts"
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

    print(request.user)
    print(request.user.is_authenticated)

    context = {
        "current_page":current_page,
        "title":title,
    }

    return render(request,"post_list.html",context)

@login_required
def post_create(request):
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
        form = PostForm()
    context = {
        "form":form,
    }
    return render(request,"post_create.html",context)

@login_required
def post_update(request,id,slug):
    post = get_object_or_404(Post, id=id)
    title = "Update Draft"
    button_text = "Update Draft"
    if post.is_draft == False:
        title = "Update Post"
        button_text = "Update Post"

    if request.method == "POST":
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if post.is_draft == True:
                post.save()
                messages.success(request, 'Draft updated.')
                # return redirect('profiles:profile_drafts', id=request.user.id, slug=request.user.profile.slug )
                return redirect('posts:post_update', id=post.id, slug=post.slug )
            else:
                post.save()
                messages.success(request, 'Post updated.')
                return redirect(post)
    else:
        form = PostForm(instance=post)

    context = {
        "title":title,
        "button_text":button_text,
        "form":form,
    }
    return render(request,"post_update.html",context)

@login_required
def post_delete(request,id,slug):
    post = get_object_or_404(Post, id=id)
    # title = "Delete Draft"
    # if post.is_draft == False:
    #     title = "Delete Post"
    if post.is_draft == True:
        post.delete()
        messages.success(request, 'Draft deleted')
        return redirect('profiles:profile_drafts', id=request.user.id, slug=request.user.profile.slug )
    else:
        post.delete()
        messages.success(request, 'Post deleted')
        return redirect('profiles:profile_posts', id=request.user.id, slug=request.user.profile.slug )


def post_detail(request,id,slug):
    post = get_object_or_404(Post, id=id)
    context = {
        "post":post,
    }

    return render(request,"post_detail.html",context)

@login_required
def post_publish(request,id,slug):
    post = get_object_or_404(Post, id=id)
    if post:
        post.is_draft = False
        post.date_published = timezone.now()
        post.save()
        messages.success(request, 'Draft published')
        return redirect('profiles:profile_drafts', id=request.user.id, slug=request.user.profile.slug )
