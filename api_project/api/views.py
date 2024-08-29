from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
import rest_framework
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import viewsets
# Create your views here.

class BookList(rest_framework.generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    
class ListCreateBookView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    
@api_view(['GET'])
def get_view(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer