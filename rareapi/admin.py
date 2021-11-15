from django.contrib import admin
from rareapi.models import RareUser, Post, Category

# Register your models here.

admin.site.register(RareUser)
admin.site.register(Post)
admin.site.register(Category)
