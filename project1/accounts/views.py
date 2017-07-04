from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, LoginForm
from project1.project1.topics.models import Topic

# Create your views here.
def signup_view(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            return redirect("home")
        else:
            context = {}
            form = UserForm()
            context['form'] = form
            context['title'] = "Sign up for Viz"
            return render(request,"accounts/signup.html",context)
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect("topics:topic_follow")

def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            return redirect("home")
        else:
            context = {}
            form = LoginForm()
            context['form'] = form
            context['title'] = "Log in To Viz"
            return render(request,"accounts/login.html",context)
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect("home")


def logout_view(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            logout(request)
            return redirect("login")
        else:
            return redirect("home")
