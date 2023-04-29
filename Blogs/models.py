from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogModel(models.Model):
    blog_heading = models.CharField(max_length=200)
    blog_author = models.ForeignKey(User, on_delete=models.CASCADE)     # Using User model as foreign key here
    blog_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    # Whenever blog is created, data and time at that moment will be added automatically
    