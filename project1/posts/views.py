from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers
from .models import Post
from .forms import PostForm
from project1.project1.comments.forms import CommentForm
from project1.project1.comments.models import Comment
from django.http import QueryDict

# Create your views here.
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.filter(is_draft = False)
        title = "Latest Posts"
        comment_title = "Comments"
        comment_button_text = "Comment"
        logged_in = False
        if request.user.is_authenticated:
            logged_in = True
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
        current_user = request.user
        same_user = []
        no_comments = []
        comments_count = []
        for post in current_page.object_list:
            paginator = Paginator(post.comment_set.all(), 5) # Show 25 contacts per page
            page = request.GET.get('page')
            try:
                comments_current_page = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                comments_current_page = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                comments_current_page = paginator.page(paginator.num_pages)
            # check 1
            if post.user == current_user:
                same_user.append("True")
            else:
                same_user.append("False")
            # check2
            if post.comment_set.all().count() == 0:
                no_comments.append("True")
            else:
                no_comments.append("False")
            comments_count.append(post.comment_set.all().count())
        form = CommentForm()

        if request.is_ajax():
            print(request.is_ajax())
            comment_count = comments_current_page.object_list.count()
            list1 = []
            list2 = []
            list3 = []
            list4 = []
            list5 = []

            for comment in comments_current_page.object_list:
                list1.append(comment.user.profile.avatar.url)
                list2.append(comment.user.username)
                list3.append( comment.content)
                list4.append(comment.date_created)
                list5.append(reverse("profiles:profile_activity", kwargs={"id": comment.user.id, "slug":comment.user.profile.slug }))

            response_data = {}
            response_data['list1']= list1
            response_data['list2']= list2
            response_data['list3']= list3
            response_data['list4']= list4
            response_data['list5']= list5
            response_data['comment_count']= comment_count
            response_data['has_previous'] = comments_current_page.has_previous()
            response_data['has_next'] = comments_current_page.has_next()
            response_data['number'] = comments_current_page.number
            response_data['page_range'] = comments_current_page.paginator.page_range[-1]

            return JsonResponse(response_data,safe=False)

        context = {
            "title":title,
            "comment_title":comment_title,
            "comment_button_text":comment_button_text,
            "logged_in":logged_in,
            "current_page":current_page,
            "comments_current_page":comments_current_page,
            "same_user":same_user,
            "no_comments":no_comments,
            "comments_count":comments_count,
            "form":form,
        }

        return render(request,"post_list.html",context)
    elif request.method == "POST" and request.is_ajax():
        print(request.POST)
        post_id = request.POST.get("id")
        post = Post.objects.get(id = post_id)
        # q = request.POST.copy()
        # q.pop("id")
        #
        # print(q)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            print('hello')
            comments = post.comment_set.all()
            comments_count = comments.count()
            paginator = Paginator(comments, 5) # Show 25 contacts per page
            page = request.GET.get('page')
            try:
                comments_current_page = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                comments_current_page = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                comments_current_page = paginator.page(paginator.num_pages)

            response_data = {}
            response_data['avatar'] = comment.user.profile.avatar.url
            response_data['username'] = comment.user.username
            response_data['content'] = comment.content
            response_data['date_created'] = comment.date_created
            response_data['profile_url'] = reverse("profiles:profile_activity", kwargs={"id": comment.user.id, "slug":comment.user.profile.slug })
            response_data['comments_count'] = comments_count
            response_data['has_previous'] = comments_current_page.has_previous()
            response_data['has_next'] = comments_current_page.has_next()
            response_data['number'] = comments_current_page.number
            response_data['page_range'] = comments_current_page.paginator.page_range[-1]
            response_data['url'] = request.path
            response_data['success'] = True
            return JsonResponse(response_data,safe=False)
        else:
            print('error')
            print(form.errors)
            response_data = {}
            response_data['success'] = False
            response_data['errors'] = form.errors
            return JsonResponse(response_data,safe=False)


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


@login_required
def post_like(request,id,slug):
    post = get_object_or_404(Post, id=id)
    if post.is_draft == True:
        return redirect("posts:post_404")
    if request.GET.get('unlike'):
        post.likes -= 1
    else:
        post.likes += 1
    post.save()
    response_data = {}
    response_data['like_count'] = post.likes
    return JsonResponse(response_data,safe=False)

@login_required
def post_bookmark(request,id,slug):
    return render(request,"post_list.html",context)

@login_required
def post_dislike(request,id,slug):
    post = get_object_or_404(Post, id=id)
    if post.is_draft == True:
        return redirect("posts:post_404")
    if request.GET.get('undislike'):
        post.dislikes -= 1
    else:
        post.dislikes += 1
    post.save()
    response_data = {}
    response_data['dislike_count'] = post.dislikes
    return JsonResponse(response_data,safe=False)


def post_detail(request,id,slug):
    if request.method == "GET":
        post = get_object_or_404(Post, id=id)
        if post.is_draft == True:
            return redirect("posts:post_404")
        logged_in = False
        if request.user.is_authenticated:
            logged_in = True
        user = post.user
        current_user = request.user
        same_user = False
        if current_user == user:
            same_user = True
        comments = post.comment_set.all()
        comments_count = comments.count()
        no_comments = True
        if comments_count != 0:
            no_comments = False
        comment_title = "Comments"
        comment_button_text = "Comment"
        form = CommentForm()
        paginator = Paginator(comments, 5) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            current_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            current_page = paginator.page(paginator.num_pages)

        if request.is_ajax():
            comment_count = current_page.object_list.count()
            print(comment_count)
            list1 = []
            list2 = []
            list3 = []
            list4 = []
            list5 = []

            for comment in current_page.object_list:
                list1.append(comment.user.profile.avatar.url)
                list2.append(comment.user.username)
                list3.append( comment.content)
                list4.append(comment.date_created)
                list5.append(reverse("profiles:profile_activity", kwargs={"id": comment.user.id, "slug":comment.user.profile.slug }))

            response_data = {}
            response_data['list1']= list1
            response_data['list2']= list2
            response_data['list3']= list3
            response_data['list4']= list4
            response_data['list5']= list5
            response_data['comment_count']= comment_count
            response_data['has_previous'] = current_page.has_previous()
            response_data['has_next'] = current_page.has_next()
            response_data['number'] = current_page.number
            response_data['page_range'] = current_page.paginator.page_range[-1]
            return JsonResponse(response_data,safe=False)

        context = {
            "post":post,
            "user":user,
            "logged_in":logged_in,
            "same_user":same_user,
            "comments_count":comments_count,
            "no_comments":no_comments,
            "comment_title":comment_title,
            "comment_button_text":comment_button_text,
            "form":form,
            "current_page":current_page,
            }

        return render(request,"post_detail.html",context)


    elif request.method == "POST" and request.is_ajax():
        print(type(request.POST))
        post = get_object_or_404(Post, id=id)
        form = CommentForm(request.POST)
        print(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

            comments = post.comment_set.all()
            comments_count = comments.count()
            paginator = Paginator(comments, 5) # Show 25 contacts per page
            page = request.GET.get('page')

            try:
                current_page = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                current_page = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                current_page = paginator.page(paginator.num_pages)

            response_data = {}
            response_data['avatar'] = comment.user.profile.avatar.url
            response_data['username'] = comment.user.username
            response_data['content'] = comment.content
            response_data['date_created'] = comment.date_created
            response_data['profile_url'] = reverse("profiles:profile_activity", kwargs={"id": comment.user.id, "slug":comment.user.profile.slug })
            response_data['comments_count'] = comments_count
            response_data['has_previous'] = current_page.has_previous()
            response_data['has_next'] = current_page.has_next()
            response_data['number'] = current_page.number
            response_data['page_range'] = current_page.paginator.page_range[-1]
            response_data['url'] = request.path
            return JsonResponse(response_data,safe=False)
        else:
            print('error')


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
