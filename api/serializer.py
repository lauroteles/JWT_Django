from rest_framework import serializers
from userauth.models import Profile,User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_toker(cls,user):
        token = super().get_token(user)

        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username

        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only= True,required=True)

    class Meta:
        model = User
        fields = ['full_name','email','password','password2']
    def validate(self, attr):
        if attr['password'] != attr['password2']:
            raise serializers.ValidationError({"password":"Password fields didn't match"})
        return attr
    
    def create(self, validate_data):
        user = User.objects.create(
            full_name=validate_data['full_name'],
            email=validate_data['email'],
        )
        email_username, username, _ = user.email.split("@")
        user.username = email_username
        user.set_password(validate_password['password'])
        user.save()
        
        return user



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model  = User
        fields = '__all__' 


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"