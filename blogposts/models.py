from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.

# class User(models.Model):
#     user_id = models.IntegerField(default=0)
#     username = models.CharField(max_length=12)
#     user_password = models.CharField(max_length=12)

class Post(models.Model):
    content = models.CharField(max_length=300)
    title = models.CharField(max_length=50, default = 'title example')
    published_date = models.DateTimeField('published date', default = timezone.now)
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    liked_users = ArrayField(models.IntegerField(default=0), default = list)
    tags = TaggableManager(blank=True)
    def __str__(self):
        return self.content
    def get_absolute_url(self):
        return reverse('blogposts:detail', args=[self.id])

class Comment(models.Model):
    comment_text = models.CharField(max_length=200)
    published_date = models.DateTimeField('published date')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return self.comment_text

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)
    def __str__(self):
        return f'Profile for user {self.user.username}'
