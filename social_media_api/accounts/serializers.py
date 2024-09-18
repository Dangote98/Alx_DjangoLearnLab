from rest_framework import serializers
from .models import CustomUser
from rest_framework.validators import ValidationError
from datetime import date

#create a userserializer with the fields from the model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email','id','first_name','last_name','date_of_birth','bio','profile_picture']
    #do some data validation to ensure that the date of birth is never in the present or the future.
    def validate_date_of_birth(self,value):
        if value >= date.today():
            raise ValidationError('date cannot be today or future. Please give the correct date')
        return value
class UserProfileSerializer(serializers.ModelSerializer):
    username= serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    date_of_birth = serializers.DateField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ["email","bio","profile_picture",'id','date_of_birth','username','first_name','last_name']