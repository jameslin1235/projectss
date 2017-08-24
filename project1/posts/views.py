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
from django.contrib import messages
from .models import Post
from project1.project1.tags.models import Tag
from .forms import PostForm

# Create your views here.
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.all()
    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            if "draft" in request.POST:
                post.save()
                messages.success(request, "Draft created.")
                return redirect("profile_drafts")
            else:
                post.date_published = timezone.now()
                post.save()
                messages.success(request, 'Post published.')
                return redirect(post)
        else:
            print('error')

def post_detail(request, pk):
    if request.method == "GET":  #post detail
        post = get_object_or_404(Post, pk=pk)
        if post.date_published is None:
            raise PermissionDenied
        else:
            context = {}
            context['post'] = post
            context['user'] = post.user
            # if request.user.is_authenticated and request.user != post.user:
            #     context['liked_post'] = request.user.profile.liked_post(post)
            return render(request,"post_detail.html",context)
    elif request.method == "PATCH" and request.is_ajax():
        post = Post.objects.get(pk = pk)
        put = QueryDict(request.body)
        if "publish" in put:
            post.date_published = timezone.now()
            post.save()
            messages.success(request, "Post published.")
            response = {}
            response['url'] = post.get_absolute_url()
            return JsonResponse(response)
        else:
            form = PostForm(put, instance=post)
            if form.is_valid():
                form.save()
                if post.date_published is None:
                    messages.success(request, "Draft updated.")
                    response = {}
                    response['url'] = reverse("posts:post_drafts")
                    return JsonResponse(response)
                else:
                    print('e')
            else:
                print('error')
    elif request.method == "DELETE" and request.is_ajax():
        post = Post.objects.get(pk = pk)
        post.delete()
        if post.date_published is None:
            messages.success(request, "Draft deleted.")
        else:
            messages.success(request, "Post deleted.")
        response = {}
        return JsonResponse(response)

@login_required
def post_create(request):
    if request.method == "GET":
        context = {}
        context['form'] = PostForm()
        return render(request,"post_create.html",context)


@login_required
def post_edit(request, pk):
    if request.method == "GET":
        post = get_object_or_404(Post, pk=pk)
        if post.user == request.user:
            context = {}
            context['form'] = PostForm(instance=post)
            context['post'] = post
            return render(request,"post_edit.html",context)
        else:
            raise PermissionDenied
