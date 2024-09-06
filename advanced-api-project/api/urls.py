from django.urls import path
from .views import CreateView,ListView,DeleteView,UpdateView,DetailView
urlpatterns = [
    path('',CreateView.as_view()),
    path('listview/',ListView.as_view()),
    path('deleteview/<int:pk>/',DeleteView.as_view()),
    path('updateview/<int:pk>/',UpdateView.as_view()),
    path('detailview/<int:pk>/',DetailView.as_view()),
]
