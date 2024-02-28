from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.urls import reverse


User = get_user_model()

# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(label="Email")
#     password1 = forms.PasswordInput()
    
#     class Meta(UserCreationForm.Meta):
#         model = User


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    is_approved = forms.BooleanField(label="Is Approved", required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'is_approved')
