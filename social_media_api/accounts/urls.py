from django.urls import path,include
from .views import login,signup,UserProfileView
urlpatterns = [
    path('register/',signup,name='signup'),
    path('login/',login,name='login'),
    path('userprofile/',UserProfileView.as_view(),name='userprofile'),
    path('api_auth/',include('rest_framework.urls'),name='auth'),
]
