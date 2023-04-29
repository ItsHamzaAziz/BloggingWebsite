from django.contrib import admin
from .models import *

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ('blog_author', 'blog_heading')

admin.site.register(BlogModel, BlogAdmin)