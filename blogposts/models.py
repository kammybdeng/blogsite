from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

# class User(models.Model):
#     user_id = models.IntegerField(default=0)
#     username = models.CharField(max_length=12)
#     user_password = models.CharField(max_length=12)

class Post(models.Model):
    content = models.CharField(max_length=300)
    published_date = models.DateTimeField('published date', default = timezone.now)
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    liked_users = ArrayField(models.IntegerField(default=0), default = list)
    def __str__(self):
        return self.post_text

class Comment(models.Model):
    comment_text = models.CharField(max_length=200)
    published_date = models.DateTimeField('published date')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return self.comment_text
