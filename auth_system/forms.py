from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'avatar', 'birth_date', 'gender', 'phone_number')