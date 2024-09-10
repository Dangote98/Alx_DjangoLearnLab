from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm,UserDetailForm,ProfileChangeForm
from django.http import HttpResponseForbidden,HttpResponse
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import UserProfile
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('profile')
        else:
            return HttpResponseForbidden("Form data incorrect")
    else:
        form = CustomUserCreationForm()
    context = {"form":form}
    return render(request,'blog/register.html',context)
def home(request):
    context = {}
    return render(request,'blog/home.html',context)
class LoginUser(LoginView):
    template_name = 'blog/login.html'
class LogoutUser(LogoutView):
    template_name = 'blog/logout.html'
@login_required(login_url='login')
def profileview(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    if request.method == 'POST':
        user_update_form = UserDetailForm(request.POST,instance=request.user)
        profile_update_form = ProfileChangeForm(request.POST,instance=user_profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            return redirect('profile')
        else:
            return HttpResponseForbidden("Incorrect form format")
    else:
        user_update_form = UserDetailForm(instance=request.user)
        profile_update_form = ProfileChangeForm(instance=user_profile)
    context = {"user_update_form":user_update_form,"profile_update_form":profile_update_form}
    return render(request,'blog/profile.html',context)