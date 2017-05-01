from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",null=True,symmetrical=False)
    position = models.CharField(
        max_length=100,
        blank=True,
    )
    company = models.CharField(
        max_length=100,
        blank=True,
    )
    school = models.CharField(
        max_length=100,
        blank=True,
    )
    concentration = models.CharField(
        max_length=100,
        blank=True,
    )
    degree_type = models.CharField(
        max_length=100,
        blank=True,
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

    class Meta:
        ordering = ["-date_created"]


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
