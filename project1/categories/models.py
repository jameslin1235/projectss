from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse

# Create your models here.
class Category(models.Model):
     category = models.CharField(max_length=100)
     slug = models.SlugField(blank=True)

     def __str__(self):
         return self.category

     def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super(Category, self).save(*args, **kwargs)

     def get_absolute_url(self):
        return reverse("categories:category_detail", kwargs={"slug": self.slug})
