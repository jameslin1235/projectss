from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from project1.project1.profiles.models import Profile
# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="posts")
    likers = models.ManyToManyField(settings.AUTH_USER_MODEL,through='PostUser',related_name="liked_posts")
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(null=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs) # Call the "real" save() method.

    def get_absolute_url(self):
        return reverse("posts:post_detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("posts:post_edit", kwargs={"id": self.id})

    # def get_comments_count(self):
    #     return self.comments.count()
    #
    # def get_comments(self):
    #     return self.comments.all()
    #
    # def get_likers_count(self):
    #     return self.likes
    #
    # def get_likers(self):
    #     return self.likers.order_by("like")

class PostUser(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_liked = models.DateTimeField()
