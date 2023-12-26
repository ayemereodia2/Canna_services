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
from cannassaince.settings import GeneralSettings
from .models import CustomUser
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


class FacebookLogin(APIView):
    """
    The view for the login by Facebook.
    """

    serializer_class = FacebookLoginSerializer

    @staticmethod
    def handle_exception(error: str) -> HttpResponsePermanentRedirect:
        params = urlencode({"error": error})
        error_redirect_uri = f"{GeneralSettings().BASE_FRONTEND_URL}?{params}"
        return redirect(error_redirect_uri)

    @classmethod
    def initialize_user(cls, user_data: Dict[str, str]):
        user, created = CustomUser.objects.get_or_create(
            user_id=user_data["id"]
        )
        if created:
            if CustomUser.objects.filter(email=user_data["email"]).exists():
                logger.error("Email already exists, provide a new email.")
                raise cls.handle_exception(
                    "Email already exists, provide a new email."
                )

            user.email = user_data["email"]
            user.username = name_to_username(user_data["name"])
            user.save()

        return user

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        code = validated_data.get("code")
        error = validated_data.get("error")
        state = validated_data.get("state")

        if error or not code:
            logger.error("An error occured getting facebook code")
            return self.handle_exception(error)

        try:
            access_token = Facebook.get_facebook_access_token(code=code)
            logger.info("facebook access token retrieved")
            return self.login_user(access_token, state)
        except OAuthErrorException as e:
            logger.error(
                "An error occured while getting facebook access token"
            )
            return self.handle_exception(e.args[0])

    @classmethod
    def login_user(cls, access_token: str, state: str):
        user_data = Facebook.get_facebook_user_info(
            access_token=access_token,
        )

        user = cls.initialize_user(user_data)

        refresh = RefreshToken.for_user(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "state": state,
        }
        token_serializer = TokenSerializer(data=data)
        token_serializer.is_valid(raise_exception=True)
        token_params = urlencode(token_serializer.data)
        redirect_uri = f"{GeneralSettings().BASE_FRONTEND_URL}?{token_params}"
        return redirect(redirect_uri)
