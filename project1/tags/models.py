from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.conf import settings
from project1.project1.posts.models import Post

# Create your models here.
def get_upload_location(instance, filename):
    return "tag"

class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    image = models.ImageField(
        upload_to = get_upload_location,
        null=True
    )
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,symmetrical=False,blank=True,through='TagUser',related_name="followed_tags")
    posts = models.ManyToManyField(Post,symmetrical=False,blank=True,through='TagPost',related_name="tags")
    general = models.BooleanField(default = False)
    nav = models.BooleanField(default = False)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tags:tag_detail", kwargs={"id": self.id, "slug": self.slug})
    #
    def get_posts(self):
        return self.posts.filter(is_draft = False).order_by("-date_published")

    # def get_explore_url(self):
    #     return reverse("topics:topic_explore", kwargs={"id": self.id, "slug": self.slug})
    #

    #
    # def get_posts_count(self):
    #     return self.posts.filter(is_draft = False).count()

class TagUser(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_followed = models.DateTimeField()

class TagPost(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_tagged = models.DateTimeField()
