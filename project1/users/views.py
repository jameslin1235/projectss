from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
# Create your views here.
def user_list(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("home")
        else:
            context = {}
            context['form'] = form
            return render(request,"user_create.html",context)

def user_create(request):
    if request.method == "GET":
        context = {}
        context['form'] = UserForm()
        return render(request,"user_create.html",context)

def home(request):
    if request.method == "GET":
        context = {}
        # if request.user.is_authenticated:
        #
        #     if request.user.profile.get_followed_tags_count() != 0:
        #         context['followed_tags'] = request.user.profile.get_followed_tags()
        # else:
        context['general_tags'] = Tag.objects.filter(general = True)
        return render(request,"home.html",context)
