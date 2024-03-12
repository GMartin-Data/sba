from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1')
