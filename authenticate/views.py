from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import LoginSerializer

# Create your views here.


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
