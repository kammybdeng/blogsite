from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager
#from django.contrib.auth import get_user_model

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
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
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

class Contact(models.Model):
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'

following = models.ManyToManyField('self',
                                   through=Contact,
                                   related_name='followers',
                                   symmetrical=False)
# Add following field to User dynamically
user_model = User
user_model.add_to_class('following',
                        models.ManyToManyField('self',
                                                through=Contact,
                                                related_name='followers',
                                                symmetrical=False))