from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .models import Author,Book
from .serializers import AuthorSerializer,BookSerializer
# Create your views here.


class CreateBookView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer