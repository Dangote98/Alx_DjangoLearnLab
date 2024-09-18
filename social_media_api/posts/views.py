from django.shortcuts import render,get_object_or_404
from .serializers import PostSerializer,CommentSerializer
from .models import Post,Comment
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import filters
User = get_user_model()
# Create your views here.
#Step 3: Create Views for CRUD Operations
# View Implementation:
# Using Django REST Framework’s viewsets, set up CRUD operations for both posts and comments in posts/views.py.
# Implement permissions to ensure users can only edit or delete their own posts and comments.
#I want to create a custom permission that will allow me to determine who can make changes and who cannot
class ReadOnlyPostComments(BasePermission):
    #I am using object permission because I want access to post and comment objects
    def has_object_permission(self, request, view, obj):
        #here I am checking whether the method include get,options, and head
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user #here, I am assigning the rights for other methods to the user if they are the author
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,ReadOnlyPostComments]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    def perform_create(self, serializer):
        #here, I want to influence what the serializer can do. I want it to save the author directly
        serializer.save(author=self.request.user)
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,ReadOnlyPostComments]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    def perform_create(self, serializer):
        #here, I want to influence what the serializer can do. I want it to save the author directly
        #here, I have added additional context to ensure I am getting the exact post. I am saying from request.data. get the post_id
        #Then, I am retrieving the post and saving it as part of the serializer
        post_id = self.request.data.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user,post=post)
    filter_backends = [filters.SearchFilter]
    search_fields = ['content']
""""
Step 5: Implement Pagination and Filtering
Enhance API Usability:
Add pagination to post and comment list endpoints to manage large datasets.
Implement filtering capabilities in post views to allow users to search posts by title or content.
"""