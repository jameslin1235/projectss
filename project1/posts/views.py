from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
# Create your views here.

def post_list(request):
    posts = Post.objects.all()

    context = {
        "posts":posts,
    }
    return render(request,"post_list.html",context)

def post_create(request):
    return HttpResponse('create')

def post_update(request):
    return HttpResponse('update')

def post_delete(request):
    return HttpResponse('delete')

def post_detail(request,id):
    post = get_object_or_404(Post, id=id)
    context = {
        "post":post,
    }

    return render(request,"post_detail.html",context)
