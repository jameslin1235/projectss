from django.shortcuts import render
from .models import Tag
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
def tag_detail(request,id,slug):
    if request.method == "GET":
        tag = get_object_or_404(Tag, id=id)
        context = {}
        context['posts'] = tag.get_posts()
        return render(request,"tag_detail.html",context)
