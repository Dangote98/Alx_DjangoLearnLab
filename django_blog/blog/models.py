from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.contrib.auth.models import User
# Create your models here.
# class UserManager(BaseUserManager):
#     def create_user(self,email,username,password,first_name,last_name):
#         if not email:
#             raise ValueError("Please provide an email")
#         if not username:
#             raise ValueError("Please provide a username")
#         user = self.model(
#             email=self.normalize_email(email),
#             username = username,
#             first_name = first_name,
#             last_name = last_name
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#     def create_superuser(self,email,username,password,first_name,last_name):
#         user = self.create_user(
#             email= self.normalize_email(email),
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             password=password
#         )
#         user.is_staff = True
#         user.is_admin = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user
# class User(AbstractUser):
#     email = models.EmailField(unique=True,max_length=155)
#     username = models.CharField(unique=True,max_length=50)
#     first_name = models.CharField(unique=False,max_length=50)
#     last_name = models.CharField(unique=False,max_length=50)
    
#     objects = UserManager()
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

class Post(models.Model):
    title = models.CharField(max_length=200, null=False, unique=True)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)