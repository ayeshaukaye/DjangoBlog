from django.contrib import admin
from blogapp.models import Post, Category, Comment, PostView, Tag

# Register your models here.

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostView)
admin.site.register(Tag)

