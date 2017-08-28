from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, QueryDict
from .forms import SessionForm

# Create your views here.
def session_list(request):
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect("home")
        else:
            context = {}
            context['form'] = form
            return render(request,"session_create.html",context)
    elif request.method == "DELETE" and request.is_ajax():
        logout(request)
        response = {}
        return JsonResponse(response)



def session_create(request):
    if request.method == "GET":
        context = {}
        context['form'] = SessionForm()
        return render(request,"session_create.html",context)
