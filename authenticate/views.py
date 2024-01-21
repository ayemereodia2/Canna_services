from .services import Facebook, OAuthErrorException, name_to_username
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, UsersSerializer, UserCreateSerializer, FacebookLoginSerializer, TokenSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework.views import APIView
import requests
from djoser.views import UserViewSet
from django.http import HttpResponsePermanentRedirect
from urllib.parse import urlencode
from social_core.backends.facebook import FacebookOAuth2

from cannassaince.settings import GeneralSettings
from .models import CustomUser
from django.views import View
from django.http import JsonResponse
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


# Create your views here.


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        user = authenticate(email=email, password=password)

        if user:
            login_serializer = self.get_serializer(data=request.data)
            if login_serializer.is_valid():
                user_serializer = UsersSerializer(user)
                return Response(
                    {
                        "access": login_serializer.validated_data["access"],
                        "refresh": login_serializer.validated_data["refresh"],
                        "user": user_serializer.data,
                        "message": "Login successful",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    login_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"message": "Invalid username or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserActivationView(APIView):
    def get(self, request, uid, token):
        protocol = "https://" if request.is_secure() else "http://"
        web_url = protocol + request.get_host()
        uid = request.args["uid"]
        uid = request.args["token"]
        post_url = web_url + "/auth/activation/"
        post_data = {"uid": uid, "token": token}
        result = requests.post(post_url, data=post_data)
        content = result.text
        return Response(content)

class RedirectSocial(View):

    def get(self, request, *args, **kwargs):
        code, state = str(request.GET['code']), str(request.GET['state'])
        json_obj = {'code': code, 'state': state}
        print(json_obj)
        return JsonResponse(json_obj)


class CustomFacebookOAuth2(FacebookOAuth2):
    REDIRECT_STATE = False
