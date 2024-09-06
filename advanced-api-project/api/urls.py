from django.urls import path
from .views import CreateBookView
urlpatterns = [
    path('',CreateBookView.as_view()),
]
