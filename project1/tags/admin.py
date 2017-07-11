from django.contrib import admin
from .models import Tag, TagUser, TagPost
# Register your models here.
admin.site.register(Tag)
admin.site.register(TagUser)
admin.site.register(TagPost)
