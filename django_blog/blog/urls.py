from django.urls import path
from .views import profileview,register,LoginUser,LogoutUser,home,CreatePostView,ListPostView,UpdatePostView,DeletePostView,DetailPostView


urlpatterns = [
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('login/',LoginUser.as_view(),name='login'),
    path('logout/',LogoutUser.as_view(next_page='/'),name='logout'),
    path('profile/',profileview,name='profile'),
    path('post/new/',CreatePostView.as_view(), name='post_form'),
    path('posts/',ListPostView.as_view(),name='post_list'),
    path('post/<int:pk>/update/',UpdatePostView.as_view(), name='edit_post'),
    path('post/<int:pk>/delete/',DeletePostView.as_view(),name='post_confirm_delete'),
    path('post/<int:pk>/',DetailPostView.as_view(),name='post_detail'),
]
