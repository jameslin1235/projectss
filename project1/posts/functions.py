from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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


def get_user_status(*args):
    current_user = args[0]
    user = args[1]
    # anonymous user
    logged_in = False
    user_status = "anonymous"

    # logged-in user
    if current_user.is_authenticated:
        logged_in = True
        if current_user == user:
            user_status = "self"
        else:
            user_status = "user"
    return logged_in, user_status