from .models import Tag
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from project1.project1.users.forms import UserForm

# Create your views here.
def tag_detail(request,pk):
    if request.method == "GET":
        tag = get_object_or_404(Tag, id=id)
        context = {}
        context['tag'] = tag
        context['related_tags'] = tag.get_related_tags()
        paginator = Paginator(tag.get_latest_posts(), 10) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            latest_posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            latest_posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            latest_posts = paginator.page(paginator.num_pages)
        context['latest_posts'] = latest_posts
        return render(request,"tag_detail.html",context)


def tag_list(request):
    if request.method == "GET":
        return render(request,"tag_detail.html")

def tag_demo(request):
    if request.method == "GET":
        context = {}
        context['form'] = UserForm()
        return render(request,"tag_demo.html",context)
