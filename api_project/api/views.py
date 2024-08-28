from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
import rest_framework
from rest_framework.generics import ListCreateAPIView
# Create your views here.

class BookList(rest_framework.generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    
class ListCreateBookView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer