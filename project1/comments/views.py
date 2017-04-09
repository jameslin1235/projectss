from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from .models import Comment
# Create your views here.

@login_required
def comment_edit(request,id,slug):
    comment = get_object_or_404(Comment, id=id)
    title = "Edit Comment"
    button_text = "Edit Comment"
    user = comment.user
    current_user = request.user
    if current_user != user:
        return redirect("posts:post_404")
    else:
        if request.method == "POST":
            form = CommentForm(request.POST,instance=comment)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.save()
                messages.success(request, "Comment edited.")
                return redirect("comments:comment_edit", id=id, slug=slug )
        else:
            form = CommentForm(instance=comment)
    context = {
        "title":title,
        "button_text":button_text,
        "form":form,
    }
    return render(request,"comment_edit.html",context)

@login_required
def comment_delete(request,id,slug):
    comment = get_object_or_404(Comment, id=id)
    user = comment.user
    current_user = request.user
    if current_user != user:
        return redirect("posts:post_404")
    else:
        comment.delete()
        messages.success(request, "Comment deleted.")
        return redirect("profiles:profile_comments", id=user.id, slug=user.profile.slug )
