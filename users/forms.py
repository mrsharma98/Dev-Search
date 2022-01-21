from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
  # UserCreationForm -- gives us a basic form with username password like we have in admin user

  class Meta:
    model = User
    fields = ['first_name', 'email', 'username', 'password1', 'password2']
    
    # To change the label
    labels = {
      'first_name': 'Name',
    }



