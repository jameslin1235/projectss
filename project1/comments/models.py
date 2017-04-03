from django.db import models
from django.utils.text import slugify
from django.conf import settings
from project1.project1.posts.models import Post

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    slug = models.SlugField()

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
       self.slug = slugify(self.content)
       super(Comment, self).save(*args, **kwargs)
