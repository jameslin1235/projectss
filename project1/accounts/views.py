from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegisterForm
# Create your views here.

def register(request):
    title = "Register"
    button_text = "Register"
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            messages.success(request, 'User created.')
            return redirect('login')
        # else:

    else:
        form = RegisterForm()

    context = {
        "title":title,
        "button_text":button_text,
        "form":form,
    }

    return render(request,"registration/register.html",context)
