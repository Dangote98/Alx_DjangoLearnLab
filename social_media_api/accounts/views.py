from django.shortcuts import render,get_object_or_404
from .models import CustomUser
from .serializers import UserSerializer,UserProfileSerializer,LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
# Create your views here.
#use a function view with an api decorator to signup
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    #check validity of serializer
    if serializer.is_valid():
        serializer.save()
        #get the user
        user = CustomUser.objects.get(email=request.data['email'])
        #use django set password to hash the password from user
        user.set_password(request.data['password'])
        user.save()
        #get the token by creating it and assigning user to current user
        token,created = Token.objects.get_or_create(user=user)
        #here we return response containing json details, such as token key and serializer data
        return Response({"token":token.key,"user":serializer.data})
@api_view(['POST'])
def signup_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = get_user_model().objects.get(email=request.data["email"])
        user.set_password(request.data['password'])
        user.save()
        return Response({"user":serializer.data})
@api_view(['POST'])
#allow user login
def login(request):
    user = get_object_or_404(CustomUser,email=request.data['email'])
    #first we check whether user has entered the right password
    if not user.check_password(request.data['password']):
        return Response({"details":"not found"},status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    #we return user details
    serializer = UserSerializer(instance=user)
    return Response({"token":token.key,"user":serializer.data})
#an alternative login version where logic is inside serializer.py
@api_view(["POST"])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data)
    return Response(serializer.errors)
class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated] #It ensures that the user is authenticated so that we can get the token
    
    def get_object(self): #returns the profile of the user
        return self.request.user