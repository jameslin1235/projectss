from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse

# Create your models here.
def get_upload_location(instance, filename):
    return "topic"

class Topic(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    image = models.ImageField(
        upload_to = get_upload_location,
        blank=True
    )
    description = models.TextField()
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Topic, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("topics:topic_detail", kwargs={"id": self.id, "slug": self.slug})

    def get_posts(self):
        return self.posts.filter(is_draft = False).order_by("-date_published")

    def get_posts_count(self):
        return self.posts.filter(is_draft = False).count()
