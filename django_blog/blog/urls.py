from django.urls import path
from .views import profileview,register,LoginUser,LogoutUser,home


urlpatterns = [
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('login/',LoginUser.as_view(),name='login'),
    path('logout/',LogoutUser.as_view(next_page='/'),name='logout'),
    path('profile/',profileview,name='profile'),
]
