from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from project1.project1.topics.models import Topic
from project1.project1.profiles.models import Profile
# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="posts")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="posts")
    likers = models.ManyToManyField(settings.AUTH_USER_MODEL,null=True,through='Like',related_name="liked_posts")
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(null=True)
    likes = models.IntegerField(default=0)
    is_draft = models.BooleanField(default=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.title = self.title.title()
        super(Post, self).save(*args, **kwargs) # Call the "real" save() method.

    def get_absolute_url(self):
        return reverse("posts:post_detail", kwargs={"id": self.id, "slug": self.slug})

    def get_comments_count(self):
        return self.comments.count()

    def get_comments(self):
        return self.comments.all()

    def get_likers_count(self):
        return self.likes

    def get_likers(self):
        return self.likers.order_by("like")


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_liked = models.DateTimeField()
