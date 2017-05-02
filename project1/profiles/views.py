from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.utils import timezone
from project1.project1.posts.models import Post
from project1.project1.comments.models import Comment
from project1.project1.profiles.models import Profile, Extra
from project1.project1.posts.forms import PostForm
from project1.project1.comments.forms import CommentForm
from .forms import ProfileForm

# Create your views here.
def profile_activity(request,id,slug):
    title = "Activity"
    User = get_user_model()
    user = get_object_or_404(User, id = id)
    posts_count = user.post_set.filter(is_draft = False).count()
    drafts_count = user.post_set.filter(is_draft = True).count()

    context = {
        "title":title,
        "user":user,
        "posts_count":posts_count,
        "drafts_count":drafts_count,

    }

    return render(request,"profile_activity.html",context)

@login_required
def profile_follow(request,id,slug):
    if request.method == "GET":
        User = get_user_model()
        user = get_object_or_404(User, id = id)
        current_user = request.user

        # logged-in user
        if current_user.is_authenticated:
            if current_user == user:
                raise PermissionDenied;
            else:
                response_data = {}
                if current_user.profile.follows.filter(user=user).exists():

                    # current_user.profile.follows.remove(user.profile)
                    Extra.objects.get(source = current_user.profile, dest = user.profile).delete()
                    response_data['message'] = "Follow"
                    return JsonResponse(response_data,safe=False)
                else:
                    # current_user.profile.follows.add(user.profile)
                    user_profile = user.profile
                    current_user_profile = current_user.profile
                    Extra.objects.create(source = current_user_profile, dest = user_profile, date_followed = timezone.now())
                    response_data['message'] = "Followed"
                    return JsonResponse(response_data,safe=False)
        # anonymous user
        else:
            raise PermissionDenied;


def profile_posts(request,id,slug):
    if request.method == "GET":
        User = get_user_model()
        user = get_object_or_404(User, id = id)
        current_user = request.user
        # anonymous user
        follow_button_text = "Follow"
        logged_in = False
        is_user = False

        # logged-in user
        if current_user.is_authenticated:
            logged_in = True
            if current_user == user:
                is_user = True
            else:
                is_user = False
                if current_user.profile.follows.filter(user= user).exists():
                    follow_button_text = "Followed"

        posts = user.post_set.filter(is_draft = False).order_by("-date_created")
        option = 1
        if request.GET.get('option'):
            option = int(request.GET.get('option'))
            if option == 1:
                posts = user.post_set.filter(is_draft = False).order_by("-date_created")

            elif option == 2:
                posts = user.post_set.filter(is_draft = False).order_by("-date_edited")

            elif option == 3:
                posts = user.post_set.filter(is_draft = False).order_by("-date_published")

            elif option == 4:
                posts = user.post_set.filter(is_draft = False).order_by("-likes")

            elif option == 5:
                posts = user.post_set.filter(is_draft = False).order_by("-dislikes")

            elif option == 6:
                posts = user.post_set.filter(is_draft = False).annotate(num_comments=Count('comment')).order_by('-num_comments')

        posts_count = posts.count()
        drafts_count = user.post_set.filter(is_draft = True).count()
        no_posts = True
        if posts_count != 0:
            no_posts = False
        title = "Posts"
        comment_title = "Comments"
        comment_button_text = "Comment"
        paginator = Paginator(posts, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            current_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            current_page = paginator.page(paginator.num_pages)

        comments_count = []
        for post in current_page.object_list:
            comments_count.append(post.comment_set.all().count())
        form = CommentForm()
        current_url = request.path

        context = {
            "user":user,
            "logged_in":logged_in,
            "is_user":is_user,
            "posts_count":posts_count,
            "drafts_count":drafts_count,
            "no_posts":no_posts,
            "title":title,
            "comment_title":comment_title,
            "comment_button_text":comment_button_text,
            "current_page":current_page,
            "comments_count":comments_count,
            "form":form,
            "current_url":current_url,
            "option":option,
            "follow_button_text":follow_button_text,
        }

        if request.is_ajax():
            template = "profile_posts_page.html"
        else:
            template = "profile_posts.html"

        return render(request,template,context)

# when you first come to page, you should be in first filter
#when you click on a different option, send a request to view to get template with filter


def profile_drafts(request,id,slug):
    if request.method == "GET":
        User = get_user_model()
        user = get_object_or_404(User, id = id)
        current_user = request.user

        follow_button_text = "Follow"
        logged_in = False
        is_user = False

        # logged-in user
        if current_user.is_authenticated:
            logged_in = True
            if current_user == user:
                is_user = True
                drafts = user.post_set.filter(is_draft = True).order_by("-date_created")
                option = 1

                if request.GET.get('option'):
                    option = int(request.GET.get('option'))
                    if option == 1:
                        drafts = user.post_set.filter(is_draft = True).order_by("-date_created")

                    elif option == 2:
                        drafts = user.post_set.filter(is_draft = True).order_by("-date_edited")


                drafts_count = drafts.count()
                posts_count = user.post_set.filter(is_draft = False).count()
                no_drafts = True
                if drafts_count != 0:
                    no_drafts = False
                title = "Drafts"
                paginator = Paginator(drafts, 10) # Show 25 contacts per page
                page = request.GET.get('page')
                try:
                    current_page = paginator.page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    current_page = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    current_page = paginator.page(paginator.num_pages)
                form = CommentForm()
                current_url = request.path

                context = {
                    "user":user,
                    "is_user":is_user,
                    "logged_in":logged_in,
                    "drafts_count":drafts_count,
                    "posts_count":posts_count,
                    "no_drafts":no_drafts,
                    "title":title,
                    "current_page":current_page,
                    "form":form,
                    "current_url":current_url,
                    "option":option,
                }

                if request.is_ajax():
                    template = "profile_drafts_page.html"
                else:
                    template = "profile_drafts.html"

                return render(request,template,context)

            else:
                raise PermissionDenied;

        # anonymous user
        else:
            raise PermissionDenied;




def profile_comments(request,id,slug):
    title = "Comments"
    User = get_user_model()
    user = User.objects.get(id = id)
    current_user = request.user
    is_user = True
    if current_user != user:
        is_user = False
    comments = Comment.objects.filter(user__id = id)
    comments_count = comments.count()
    no_comments = True
    if comments_count != 0:
        no_comments = False

    paginator = Paginator(comments, 5) # Show 25 contacts per page
    page = request.GET.get("page")
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
        "user":user,
        "is_user":is_user,
        "comments_count":comments_count,
        "no_comments":no_comments,
        "current_page":current_page,
    }

    return render(request,"profile_comments.html",context)

def profile_bookmarks(request,id,slug):
    title = "Bookmarks"
    User = get_user_model()
    user = User.objects.get(id = id)
    context = {
        "title":title,
        "user":user,
    }

    return render(request,"profile_bookmarks.html",context)


def profile_following(request,id,slug):
    if request.method == "GET":
        User = get_user_model()
        user = User.objects.get(id = id)
        current_user = request.user

        # anonymous user
        top_follow_button_text = "Follow"
        bottom_follow_button_text = "Follow"
        logged_in = False
        is_user = False

        # logged-in user
        if current_user.is_authenticated:
            logged_in = True
            if current_user == user:
                is_user = True
                bottom_follow_button_text = "Followed"
            else:
                is_user = False
                if current_user.profile.follows.filter(user=user).exists():
                    top_follow_button_text = "Followed"

        profile_url = user.profile.get_absolute_url()
        current_url = request.path

        following = user.profile.follows.all().order_by()
        #find time Followed
        user.profile.
        following_count = following.count()
        drafts_count = user.post_set.filter(is_draft = True).count()
        posts_count = user.post_set.filter(is_draft = False).count()
        no_following = True
        if following_count != 0:
            no_following = False
        title = "Following"
        paginator = Paginator(following, 10) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            current_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            current_page = paginator.page(paginator.num_pages)

        follow_status = []
        follow_me = []
        if current_user.is_authenticated:
            if current_user != user:
                for following in current_page:
                    if following.user == current_user:
                        follow_me.append(True)
                    else:
                        follow_me.append(False)
                    if current_user.profile.follows.filter(user=following.user).exists():
                        follow_status.append("Followed")
                    else:
                        follow_status.append("Follow")


        context = {
            "user":user,
            "current_user":current_user,
            "top_follow_button_text":top_follow_button_text,
            "bottom_follow_button_text":bottom_follow_button_text,
            "logged_in":logged_in,
            "is_user":is_user,
            "profile_url":profile_url,
            "following_count":following_count,
            "drafts_count":drafts_count,
            "posts_count":posts_count,
            "no_following":no_following,
            "title":title,
            "current_page":current_page,
            "follow_status":follow_status,
            "follow_me":follow_me,
        }

        return render(request,"profile_following.html",context)


def profile_followers(request,id,slug):

    title = "Followers"
    User = get_user_model()
    user = User.objects.get(id = id)
    context = {
        "title":title,
        "user":user,
    }

    return render(request,"profile_followers.html",context)

@login_required
def profile_edit(request,id,slug):
    title = "Edit Profile"
    button_text = "Edit Profile"
    User = get_user_model()
    user = User.objects.get(id = id)
    profile = user.profile
    current_user = request.user
    if current_user != user:
        return redirect("posts:post_404")
    else:
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES, instance = profile)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                messages.success(request, 'Profile edited.')
                return redirect('profiles:profile_edit', id=user.id, slug=user.profile.slug )
        else:
            form = ProfileForm(instance = profile)
    context = {
        "title":title,
        "button_text":button_text,
        "form":form,
    }
    return render(request,"profile_edit.html",context)
