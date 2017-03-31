from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import Category
from project1.project1.posts.models import Post
# Create your views here.


def category_list(request):
    categories = Category.objects.all()
    title = "Categories"
    context = {
        "categories":categories,
        "title":title,
    }
    return render(request,"category_list.html",context)


def category_detail(request,slug):
    category_posts = Post.objects.filter(category__slug = slug)
    title = slug.title()
    paginator = Paginator(category_posts, 5) # Show 25 contacts per page
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
        "title":title,
    }

    return render(request,"category_detail.html",context)
