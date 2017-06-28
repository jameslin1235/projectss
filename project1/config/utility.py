from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from project1.project1.profiles.models import Profile
from django.shortcuts import render

def paginate(*args):
    comments = args[0][0]
    objects_count = args[0][1]
    request = args[0][2]
    paginator = Paginator(comments, objects_count) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        current_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        current_page = paginator.page(paginator.num_pages)

    num_pages = paginator.num_pages
    if num_pages == 1:
        is_pagination = False
        page_num = 0
    else:
        is_pagination = True
        page_num = []
        page_range = paginator.page_range
        first_page_num = page_range[0]
        last_page_num = page_range[-1]
        current_page_num = current_page.number
        pagination_last_callback_args = [current_page_num,page_num,first_page_num]
        pagination_first_callback_args = [current_page_num,page_num,last_page_num]
        pagination_other_callback_args = [current_page_num,page_num,first_page_num,last_page_num]

        if current_page_num == first_page_num:
            page_num.append(first_page_num)
            pagination_first(pagination_first_callback_args)
        elif current_page_num == last_page_num:
            page_num.append(last_page_num)
            pagination_last(pagination_last_callback_args)
        else:
            page_num.append(current_page_num)
            pagination_other(pagination_other_callback_args)

    return current_page, is_pagination, page_num

def pagination_other(*args):
    current_page_num = args[0][0]
    page_num = args[0][1]
    first_page_num = args[0][2]
    last_page_num = args[0][3]
    if current_page_num + 1 == last_page_num:
        page_num.append(last_page_num)
    else:
        page_num.append(current_page_num + 1)
        if current_page_num + 2 != last_page_num:
            page_num.append(-1)
        page_num.append(last_page_num)
    if current_page_num - 1 == first_page_num:
        page_num.insert(0,first_page_num)
    else:
        page_num.insert(0,current_page_num - 1)
        if current_page_num - 2 != first_page_num:
            page_num.insert(0,-1)
        page_num.insert(0,first_page_num)


def pagination_first(*args):
    current_page_num = args[0][0]
    page_num = args[0][1]
    last_page_num = args[0][2]
    counter = 0
    for i in range(1,4):
        if current_page_num + i == last_page_num:
            page_num.append(last_page_num)
            break
        else:
            page_num.append(current_page_num + i)
            counter += 1
    if counter == 3:
        if current_page_num + 4 != last_page_num:
            page_num.append(-1)
        page_num.append(last_page_num)

def pagination_last(*args):
    current_page_num = args[0][0]
    page_num = args[0][1]
    first_page_num = args[0][2]
    counter = 0
    for i in range(1,4):
        if current_page_num - i == first_page_num:
            page_num.insert(0,first_page_num)
            break
        else:
            page_num.insert(0,current_page_num - i)
            counter += 1
    if counter == 3:
        if current_page_num - 4 != first_page_num:
            page_num.insert(0,-1)
        page_num.insert(0,first_page_num)

def get_user_status(user,current_user):
    user_status = ["self" if current_user == user else "user" if current_user.is_authenticated else "anonymous"]
    return user_status[0]

# def get_logged_in_status (current_user):
#     logged_in_status = [True if current_user.is_authenticated else False]
#     return logged_in_status[0]

# def get_user_edit_status(user_status):
#     user_edit_status = [True if user_status == "self" else False]
#     return user_edit_status[0]

# def get_user_message_status(user_status):
#     user_message_status = [True if user_status != "self" else False]
#     return user_message_status[0]

def get_user_follow_status(user,current_user,user_status):
    if user_status == "anonymous":
        user_follow_status = "Follow"
    else:
        if current_user.profile.followed_user(user):
            user_follow_status = "Followed"
        else:
            user_follow_status = "Follow"
    return user_follow_status

# def get_user_profile_status(user):
#     fields_names = [field.name for field in Profile._meta.get_fields() if field.name.startswith("profile_")]
#     fields_values = Profile.objects.filter(id=user.id).values(*fields_names)
#     fields_values_dict = fields_values[0]
#     user_profile_status  = [True if fields_values_dict else False]
#     return user_profile_status[0]
# 
# def get_user_profile_fields(user):
#     fields_names = [field.name for field in Profile._meta.get_fields() if field.name.startswith("profile_")]
#     fields_values = Profile.objects.filter(id=user.id).values(*fields_names)
#     fields_values_dict = fields_values[0]
#     fields_values_list = [[field,value] for field, value in fields_values_dict.items() if value != None and value != '' ]
#     return fields_values_list


def get_user_posts_like_status(*args):
    user_status = args[0][0]
    current_user = args[0][1]
    current_page = args[0][2]
    user_posts_like_status = []
    for post in current_page.object_list:
        if user_status == "anonymous":
            user_posts_like_status.append("No")
        elif user_status =="self":
            user_posts_like_status.append("No")
        elif user_status == "user":
            if current_user.profile.liked_post(post):
                user_posts_like_status.append("Liked")
            else:
                user_posts_like_status.append("No")
    return user_posts_like_status


def get_user_posts_dislike_status(*args):
    user_status = args[0][0]
    current_user = args[0][1]
    current_page = args[0][2]
    user_posts_dislike_status = []
    for post in current_page.object_list:
        if user_status == "anonymous":
            user_posts_dislike_status.append("No")
        elif user_status =="self":
            user_posts_dislike_status.append("No")
        elif user_status == "user":
            if current_user.profile.disliked_post(post):
                user_posts_dislike_status.append("Disliked")
            else:
                user_posts_dislike_status.append("No")
    return user_posts_dislike_status

def get_like_dislike_buttons_status(*args):
    user_status = args[0][0]
    current_page = args[0][1]
    like_dislike_buttons_status = []
    for post in current_page.object_list:
        if user_status == "anonymous":
            like_dislike_buttons_status.append("Enabled")
        elif user_status =="self":
            like_dislike_buttons_status.append("Disabled")
        elif user_status == "user":
            like_dislike_buttons_status.append("Enabled")
    return like_dislike_buttons_status

def get_user_posts_comments_count(*args):
    current_page = args[0][0]
    comments_count = []
    for post in current_page.object_list:
        comments_count.append(post.get_comments_count())
    return comments_count




def get_modal(request):
    if request.method == "GET" and request.is_ajax():
        template = request.GET.get("template")
        return render(request,template)


def get_alert(request):
    if request.method == "GET" and request.is_ajax():
        if request.GET:
            template = "alert.html"
            message = request.GET.get("message")
            context = {"message":message}
            return render(request,template,context)

def get_error(request):
    if request.method == "GET" and request.is_ajax():
            template = "form_error.html"
            value = request.GET.get("value")
            context = {"value":value}
            return render(request,template,context)


def get_loader(request):
    if request.method == "GET" and request.is_ajax():
        template = "loading_gif.html"
        return render(request,template)
