import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

countries_path = os.path.join(settings.BASE_DIR, "project1/static/data/countries.txt")
print(countries_path)
with open(countries_path) as f:
    for line in f:
        countries_tuple = tuple(tuple(i.rstrip('\n').split(':')) for i in f)


# Create your models here.
class Profile(models.Model):
    residence_choices = countries_tuple
    print(residence_choices)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    following = models.ManyToManyField("self",null=True,symmetrical=False, through='Follow', related_name="followers")
    gender = models.NullBooleanField(
        blank=True,
    )
    profile_credential = models.CharField(
        max_length = 100,
        blank=True,
    )

    profile_description = models.TextField(
        blank=True,
    )
    residence = models.CharField(
        max_length = 2,
        choices = residence_choices,
        blank = True,
    )

    avatar = models.FileField(
        upload_to = "profile_avatar/",
        blank=True,
        default="profile_avatar/1.jpg",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    slug = models.SlugField()

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

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Follow(models.Model):
    source = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name ="source")
    dest = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name= "dest")
    date_followed = models.DateTimeField()

    class Meta:
        ordering = ["-date_followed"]
