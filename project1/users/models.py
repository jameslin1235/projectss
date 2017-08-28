from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from project1.project1.tags.models import Tag

# Create your models here.

def get_upload_location(instance, filename):
    return "users/%s/%s" % (instance.user.username,filename)

class User(AbstractUser):
    gender_choices = (
        ('','Select a Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    # following = models.ManyToManyField("self", symmetrical=False, through='ProfileFollow', related_name="followers")
    # tags = models.ManyToManyField(Tag, through='ProfileTag')
    tags = models.ManyToManyField(Tag, through='UserTag')
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

    def get_absolute_url(self):
        return reverse("profiles:profile_detail", kwargs={"pk": self.pk})

class UserTag(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    date_followed = models.DateTimeField()

    def __str__(self):
        return '%s %s' % (self.user, self.tag)
