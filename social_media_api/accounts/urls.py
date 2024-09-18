from django.urls import path,include
from .views import login,signup,UserProfileView,signup_user,login_user
urlpatterns = [
    path('register/',signup,name='signup'),
    path('login/',login,name='login'),
    path('userprofile/',UserProfileView.as_view(),name='userprofile'),
    path('api_auth/',include('rest_framework.urls'),name='auth'),
    path('register_new_user/',signup_user,name='register'),
    path('login_user/',login_user,name='login_user')
]
