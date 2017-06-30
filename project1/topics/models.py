from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse

# Create your models here.
class Topic(models.Model):
    topic = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.topic

    def save(self, *args, **kwargs):
        self.slug = slugify(self.topic)
        super(Topic, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("topics:topic_detail", kwargs={"id": self.id, "slug": self.slug})

    def get_posts(self):
        return self.posts.filter(is_draft = False).order_by("-date_published")
