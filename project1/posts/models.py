from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs) # Call the "real" save() method.

    def get_absolute_url(self):
        return reverse("posts:post_detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("posts:post_edit", kwargs={"pk": self.pk})
