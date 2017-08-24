
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, QueryDict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.conf import settings
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils import timezone
from project1.project1.posts.models import Post
from project1.project1.posts.forms import PostForm
from .models import Profile
from .forms import ProfileForm, ProfileAvatarForm, ProfileBackgroundForm

# from PIL import Image

# Create your views here.
def profile_detail(request, pk):
    if request.method == "GET":
        profile = get_object_or_404(Profile, pk = pk)
        context = {}
        context['profile'] = profile
        return render(request,"profile_detail.html",context)
    elif request.method == "PATCH" and request.is_ajax():
        profile = Profile.objects.get(pk = pk)
        patch = QueryDict(request.body)
        form = ProfileForm(patch, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            response = {}
            return JsonResponse(response)
        else:
            print('error')
    elif request.method == "POST":
        profile = Profile.objects.get(pk = pk)
        if "avatar" in request.FILES:
            form = ProfileAvatarForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile avatar updated.")
                return redirect(profile)
            else:
                print('error')
        else:
            form = ProfileBackgroundForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile background updated.")
                return redirect(profile)
            else:
                print('error')

@login_required
def profile_edit(request, pk):
    if request.method == "GET":
        profile = get_object_or_404(Profile, pk=pk)
        if profile.user == request.user:
            context = {}
            context['form'] = ProfileForm(instance = profile)
            context['profile'] = profile
            return render(request,"profile_edit.html",context)
        else:
            raise PermissionDenied

@login_required
def profile_drafts(request):
    if request.method == "GET":
        drafts_count = request.user.profile.get_drafts_count()
        context = {}
        context['drafts_count'] = drafts_count
        if drafts_count != 0:
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
    return render(request,"profile_drafts.html",context)


def profile_posts(request, pk):
    if request.method == "GET":
        profile = get_object_or_404(Profile, pk = pk)
        context = {}
        context['profile'] = profile
        posts_count = profile.get_posts_count()
        context['posts_count'] = posts_count
        if posts_count != 0:
            paginator = Paginator(profile.get_posts(), 10) # Show 25 contacts per page
            page = request.GET.get('page')
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                posts = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                posts = paginator.page(paginator.num_pages)
            context['posts'] = posts
        return render(request,"profile_posts.html",context)

def profile_following(request, pk):
    return render(request,"profile_posts.html",context)

def profile_followers(request, pk):
    return render(request,"profile_posts.html",context)
