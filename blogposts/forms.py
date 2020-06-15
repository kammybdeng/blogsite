from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

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
