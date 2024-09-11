from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import Post,UserProfile
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name','username','password1', 'password2']
class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio','image_url']
class UserDetailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name','username']
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content']
    