from django.forms import ModelForm
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
