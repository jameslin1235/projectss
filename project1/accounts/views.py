from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegisterForm
# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created.')
            return redirect('login')
        # else:

    else:
        form = RegisterForm()

    context = {
        "form":form,
    }

    return render(request,"registration/register.html",context)
