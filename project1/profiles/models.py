import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.core.urlresolvers import reverse

def get_upload_location(instance, filename):
    return "users/%s/%s" % (instance.user.username,filename)

# import os
# import csv
# path1 = os.path.join(settings.BASE_DIR, "project1/static/data/countries.txt")
# path2 = os.path.join(settings.BASE_DIR, "project1/static/data/occupations.txt")
# with open(path1) as f1:
#     countries_tuple = tuple(tuple(line.rstrip('\n').split(':')) for line in f1)
#     print(countries_tuple)
#
# with open(path2) as f2:
#     occupations_tuple = tuple(('',line[1].rstrip('\n')) if line[0] == 1 else (line[1].rstrip('\n'),)*2 for line in enumerate(f2, 1))
#     print(occupations_tuple)
    # residence_choices = countries_tuple
    # occupation_choices = occupations_tuple
# Create your models here.
class Profile(models.Model):
    gender_choices = (
        ('','Select a Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    following = models.ManyToManyField("self",null=True,symmetrical=False, through='Follow', related_name="followers")
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

    def get_profile_status(self):
        fields_dict = Profile.objects.filter(id = self.id).values("gender", "credential", "description", "residence", "occupation", "position", "company", "school", "major")[0]
        for value in fields_dict.values():
            if len(value) != 0:
                return False
        return True

    def get_profile_fields(self):
        fields_dict = Profile.objects.filter(id = self.id).values("gender", "credential", "description", "residence", "occupation", "position", "company", "school", "major")[0]
        profile_fields = []
        for value in fields_dict.items():
            if len(value[1]) != 0:
                profile_fields.append(list(value))
        return profile_fields

    def liked_post(self,post):
        return self.user.liked_posts.filter(id=post.id).exists()

    def get_followed_topics(self):
        return self.user.followed_topics.all()
    # def followed_user(self, user):
    #     return self.following.filter(user=user).exists()
    #
    # def follow_user(self,profile):
    #     Follow.objects.create(source=self,dest=profile,date_followed=timezone.now())
    #     return None
    #
    # def unfollow_user(self,profile):
    #     Follow.objects.get(source=self, dest=profile).delete()
    #     return None
    #
    # def get_following_count(self):
    #     return self.following.count()
    #
    # def get_followers_count(self):
    #     return self.followers.count()


    #
    # def get_comments_count(self):
    #     return self.user.comments.count()
    #



    class Meta:
        ordering = ["-date_created"]

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



class Follow(models.Model):
    source = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name ="source")
    dest = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name= "dest")
    date_followed = models.DateTimeField()

    class Meta:
        ordering = ["-date_followed"]
