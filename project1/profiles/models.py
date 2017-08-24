import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.core.urlresolvers import reverse
from project1.project1.tags.models import Tag

def get_upload_location(instance, filename):
    return "users/%s/%s" % (instance.user.username,filename)


class Profile(models.Model):
    gender_choices = (
        ('','Select a Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # following = models.ManyToManyField("self", symmetrical=False, through='ProfileFollow', related_name="followers")
    tags = models.ManyToManyField(Tag, through='ProfileTag')
    first_login = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    gender = models.CharField(
        max_length=10,
        choices=gender_choices,
        blank=True
    )
    industry = models.CharField(
        max_length=100,
        blank=True
    )
    position = models.CharField(
        max_length=100,
        blank=True
    )
    company = models.CharField(
        max_length=100,
        blank=True
    )
    school = models.CharField(
        max_length=100,
        blank=True
    )
    concentration = models.CharField(
        max_length=100,
        blank=True
    )
    location = models.CharField(
        max_length=100,
        blank=True
    )
    credential = models.CharField(
        max_length=100,
        blank=True
    )
    description = models.TextField(
        blank=True,
    )
    avatar_width_field = models.IntegerField()
    avatar_height_field = models.IntegerField()
    avatar = models.ImageField(
        upload_to = get_upload_location,
        height_field = "avatar_height_field",
        width_field = "avatar_width_field",
        blank=True,
        default= "default/avatar.jpg"
    )
    background_width_field = models.IntegerField()
    background_height_field = models.IntegerField()
    background = models.ImageField(
        upload_to = get_upload_location,
        height_field = "background_height_field",
        width_field = "background_width_field",
        blank=True,
        default= "default/background.jpg"
    )

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs) # Call the "real" save() method.

    def get_absolute_url(self):
        return reverse("profiles:profile_detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("profiles:profile_edit", kwargs={"pk": self.pk})

    def get_posts(self):
        return self.user.posts.filter(date_published__isnull = False)

    def get_posts_count(self):
        return self.user.posts.filter(date_published__isnull = False).count()

    def get_drafts(self):
        return self.user.posts.filter(date_published__isnull = True).order_by("-date_updated")

    def get_drafts_count(self):
        return self.user.posts.filter(date_published__isnull = True).count()

    def get_followed_tags_count(self):
        return self.tags.count()

    def get_followed_tags(self):
        return self.tags.all()

    class Meta:
        ordering = ["-date_created"]

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class ProfileTag(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    date_tagged = models.DateTimeField()

    def __str__(self):
        return '%s %s' % (self.profile, self.tag)

# class ProfileFollow(models.Model):
#     source = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name ="source")
#     dest = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name= "dest")
#     date_followed = models.DateTimeField()
#
#     class Meta:
#         ordering = ["-date_followed"]
