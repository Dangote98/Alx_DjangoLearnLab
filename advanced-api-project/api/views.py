from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,DestroyAPIView,ListCreateAPIView,UpdateAPIView,RetrieveAPIView
from .models import Author,Book
from .serializers import AuthorSerializer,BookSerializer
from rest_framework.filters import OrderingFilter
from rest_framework import filters
from rest_framework.decorators import permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework import serializers
# Create your views here.

#This view allows the user to only create a book instance but cannot get or update or delete it.
#i added some validations on the view
@permission_classes([IsAuthenticated])
class CreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def create(self, request, *args, **kwargs):
        book = Book.objects.filter(title=request.data['title'])
        if book.exists():
            raise serializers.ValidationError('Book already exists')
        else:
            return super().create(request, *args, **kwargs)
@permission_classes([IsAuthenticatedOrReadOnly])
class ListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
#I have added permission classes
@permission_classes([IsAuthenticated])
class DeleteView(DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
#I have added permission classes
#i added some validations on the view
@permission_classes([IsAuthenticated])
class UpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    def update(self, request, *args, **kwargs):
        if len(request.data['title']) <5:
            raise serializers.ValidationError("The length of title cannot be less than 5 characters")
        return super().update(request, *args, **kwargs)
class DetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer