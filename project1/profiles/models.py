import os
import csv
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.utils import timezone

def upload_location(instance, filename):
    return "/users/%s/%s" %(instance.id, filename)

path1 = os.path.join(settings.BASE_DIR, "project1/static/data/countries.txt")
path2 = os.path.join(settings.BASE_DIR, "project1/static/data/occupations.txt")
with open(path1) as f1:
    countries_tuple = tuple(tuple(line.rstrip('\n').split(':')) for line in f1)
    print(countries_tuple)

with open(path2) as f2:
    occupations_tuple = tuple(('',line[1].rstrip('\n')) if line[0] == 1 else (line[1].rstrip('\n'),)*2 for line in enumerate(f2, 1))
    print(occupations_tuple)

# Create your models here.
class Profile(models.Model):
    residence_choices = countries_tuple
    occupation_choices = occupations_tuple
    gender_choices = (
        ('','Select a Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    following = models.ManyToManyField("self",null=True,symmetrical=False, through='Follow', related_name="followers")
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    profile_gender = models.CharField(
        max_length = 1,
        choices = gender_choices,
        blank=True,
    )
    profile_credential = models.CharField(
        max_length = 100,
        blank=True,
    )

    profile_description = models.TextField(
        blank=True,
    )
    profile_residence = models.CharField(
        max_length = 2,
        choices = residence_choices,
        blank = True,
    )

    profile_occupation = models.CharField(
        max_length = 100,
        choices = occupation_choices,
        blank = True,
    )

    profile_position = models.CharField(
        max_length = 100,
        blank = True,
    )

    profile_company = models.CharField(
        max_length = 100,
        blank = True,
    )
    profile_school = models.CharField(
        max_length = 100,
        blank = True,
    )
    profile_major = models.CharField(
        max_length = 100,
        blank = True,
    )
    avatar_width_field = models.IntegerField()
    avatar_height_field = models.IntegerField()
    avatar = models.ImageField(
        upload_to = upload_location,
        height_field = "avatar_height_field",
        width_field = "avatar_width_field",
        blank=True,
        default="default/avatar.jpg",
    )

    background_width_field = models.IntegerField()
    background_height_field = models.IntegerField()
    background = models.ImageField(
        upload_to = upload_location,
        height_field = "background_height_field",
        width_field = "background_width_field",
        blank=True,
        default="default/background.jpg",
    )

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs) # Call the "real" save() method.

    def get_absolute_url(self):
        return reverse("profiles:profile_activity", kwargs={"id": self.id, "slug": self.slug})

    def followed_user(self, user):
        return self.following.filter(user=user).exists()

    def follow_user(self,profile):
        Follow.objects.create(source=self,dest=profile,date_followed=timezone.now())
        return None

    def unfollow_user(self,profile):
        Follow.objects.get(source=self, dest=profile).delete()
        return None

    def get_following_count(self):
        return self.following.count()

    def get_followers_count(self):
        return self.followers.count()

    def get_posts_count(self):
        return self.user.posts.filter(is_draft = False).count()

    def get_posts(self):
        return self.user.posts.filter(is_draft = False).order_by("-date_published")

    def get_drafts_count(self):
        return self.user.posts.filter(is_draft = True).count()

    def get_comments_count(self):
        return self.user.comments.count()

    def liked_post(self,post):
        return self.liked_posts.filter(id=post.id).exists()

    def disliked_post(self,post):
        return self.disliked_posts.filter(id=post.id).exists()

    class Meta:
        ordering = ["-date_created"]

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)



class Follow(models.Model):
    source = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name ="source")
    dest = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name= "dest")
    date_followed = models.DateTimeField()

    class Meta:
        ordering = ["-date_followed"]
