
import random
from api import serializer as api_serializer
from userauth.models import User,Profile

from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics,status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings





class MyTokenObtainPairVIew(TokenObtainPairView):

    serializer_class = api_serializer.MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = api_serializer.RegisterSerializer


def generate_random_otp(length=7):
    otp = "".join([str(random.randint(0,9))for _ in range(length) ])
    
    return otp

class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes =[AllowAny]
    serializer_class = api_serializer.UserSerializer

    def get_object(self):
        email = self.kwargs['email']

        user = User.objects.filter(email=email)

        if user:    
            
            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)

            refresh_token = str(refresh.acess_token)
            user.refresh_token = refresh_token
            user.otp = generate_random_otp()

            user.save()
            
            link = f"http://localhost:5173/create-new-password/?otp{user.otp}&uuidb64={uuidb64}&=refresh_token={refresh_token}"

            context = {
                "link":link,
                "username":user.username
            }
            
            subject = "Password Reset Email"
            text_body = render_to_string("email/password_reset.txt", context)
            html_body = render_to_string("email/password_reset.html", context)

            msg = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.FROM_EMAIL,
                to=[user.eamil],
                body=text_body
            )

            msg.attach_alternative(html_body,"text/html")
            msg.send()

            print("link ======== ", link)

            return user

class PasswordChangeAPIVIew(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.UserSerializer

    def create(self,request,*args, **kwargs):
        payload = request.data

        otp = request.data['otp']
        uuidb64 = request.data['uuidb64']
        password = request.data['password']


        user = User.objects.get(id=uuidb64, otp=otp)
        if user:
            user.set_password(password)
            user.otp =''
            user.save()

            return Response({"message":"Password change sucessufully"},status=status.HTTP_201_CREATED)
        
        else:
            return Response({"message":"User doesn't exist"},status=status.HTTP_404_NOT_FOUND)