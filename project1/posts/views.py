from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
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
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created.')
            return redirect(post)
        # else:

    else:
        form = PostForm()
    context = {
        "form":form,
    }
    return render(request,"post_create.html",context)

@login_required
def post_update(request,id):
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return redirect(post)
        # else:
    else:
        form = PostForm(instance=post)

    context = {
    "form":form,
    }
    return render(request,"post_update.html",context)

@login_required
def post_delete(request,id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect("posts:post_list")


def post_detail(request,id,slug):
    post = get_object_or_404(Post, id=id)
    context = {
        "post":post,
    }

    return render(request,"post_detail.html",context)
