from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.conf import settings
from project1.project1.posts.models import Post
import operator

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField(blank=True)
    slug = models.SlugField(blank=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,symmetrical=False,blank=True,through='TagUser',related_name="followed_tags")
    posts = models.ManyToManyField(Post,symmetrical=False,blank=True,through='TagPost',related_name="tags")
    general = models.BooleanField(default = False)
    nav = models.BooleanField(default = False)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.image = "/static/img/tags/" + self.name + ".jpg/"
        super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tags:tag_detail", kwargs={"id": self.id, "slug": self.slug})
    #
    def get_posts(self):
        return self.posts.filter(is_draft = False).order_by("-date_published")

    def get_latest_posts(self):
        return self.posts.filter(is_draft = False).order_by("-date_published")

    def get_related_tags(self):
        related_posts = self.posts.filter(is_draft = False)
        result = {}
        for post in related_posts:
            for tag in post.tags.all():
                if tag != self:
                    if tag not in result:
                        result[tag] = 1
                    else:
                        result[tag] += 1
        sorted_tags = []
        for t in sorted(result.items(), key=operator.itemgetter(1), reverse=True)[:10]:
            sorted_tags.append(t[0])
        return sorted_tags
    #for every tag that appears in the same post as current tag, count #
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
