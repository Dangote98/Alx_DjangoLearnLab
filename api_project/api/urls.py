from django.urls import path
from .views import BookList, ListCreateBookView

urlpatterns = [
    path('api/books/create/',ListCreateBookView.as_view()),
    path('api/books/',BookList.as_view()),
]
