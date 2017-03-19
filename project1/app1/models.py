from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
# class Category(models.Model):
#      category = models.CharField(max_length=100)
#      slug = models.SlugField()
#
#      def __str__(self):
#          return self.category
#
#      def save(self, *args, **kwargs):
#         self.slug = slugify(self.category)
#         super(Category, self).save(*args, **kwargs)



# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     content = models.TextField()
#     date_created = models.DateTimeField(auto_now_add=True)
#     likes = models.IntegerField(default=0)
#     dislikes = models.IntegerField(default=0)
#     slug = models.SlugField()
#
#     def __str__(self):
#         return self.content
#
#     def save(self, *args, **kwargs):
#        self.slug = slugify(self.content)
#        super(Comment, self).save(*args, **kwargs)
#
# class Profile(models.Model):
#
#     GENDER = (
#         ('M', 'Male'),
#         ('F', 'Female')
#     )
#
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     age = models.IntegerField()
#     gender = models.CharField(max_length=1,choices=GENDER)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_edited = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.first_name
