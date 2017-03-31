from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=100,

    )
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
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

    class Meta:
        ordering = ["-date_created"]
