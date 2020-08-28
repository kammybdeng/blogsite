from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Post

class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length= 30, help_text = 'Required')
    # last_name = forms.CharField(max_length= 30, help_text = 'Required')
    email = forms.EmailField(max_length = 254, help_text = 'Required')

    class Meta():
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

class UserLoginForm(AuthenticationForm):
        def __init__(self, *args, **kwargs):
            super(UserLoginForm, self).__init__(*args, **kwargs)

        username = forms.CharField(max_length=30)
        password = forms.CharField(widget = forms.PasswordInput())

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
