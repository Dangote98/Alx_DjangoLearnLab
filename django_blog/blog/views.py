from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm,UserDetailForm,ProfileChangeForm,PostForm
from django.http import HttpRequest, HttpResponseForbidden,HttpResponse
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import UserProfile,Post
from django.views.generic import ListView,CreateView,DeleteView,UpdateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
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
# In this list view, the focus is on implement a view that allows all users to see all the posts\
            # The use of the loginmixin is to ensure only logged in users are allowed\
                # The login_url is placed on the settings.py
class ListPostView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    
    def get_queryset(self):
        return Post.objects.all()
# In this detail view, the focus is on implement a view that makes use of the specific post pk\
        # use of the detail operation to view details of a single post with a specific id\
            # The use of the loginmixin is to ensure only logged in users are allowed\
                # The login_url is placed on the settings.py    
class DetailPostView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    def get_queryset(self):
        return Post.objects.all()
 # In this create view, the focus is on implement a view that makes\
        # use of the create operation to create a post\
            # The use of the loginmixin is to ensure only logged in users are allowed\
                # The login_url is placed on the settings.py   
class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'blog/post_form.html'
    model = Post
    form_class = PostForm
    def form_valid(self, form):
        if form.is_valid():
            posts = form.save(commit=False)
            posts.author = self.request.user
            posts.save()
            return redirect('post_list')
        return super().form_valid(form)
    # In this delete view, the focus is on implement a view that makes\
        # use of the delete operation to delete a post with a specific id
class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
# In this update view, the focus is on implement a view that makes\
        # use of the update operation to update a post with a specific id\
            # The use of the loginmixin is to ensure only logged in users are allowed\
                # The login_url is placed on the settings.py
    

class UpdatePostView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/edit_post.html'
    def form_valid(self, form):
        if form.is_valid():
            post = form.save(commit=False)
            post.author = self.request.user
            post.save()
            
        return super().form_valid(form)
    success_url = reverse_lazy('post_list')
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    
