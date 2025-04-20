from django.contrib import admin
from blogapp.models import Post, Category, Comment

# Register your models here.

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)

