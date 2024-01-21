from urllib.parse import urlparse
from rest_framework import serializers
from djoser import serializers as djoser_serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import IntegrityError, transaction
from djoser.conf import settings
from rest_framework.response import Response
from rest_framework import status
from . import exceptions as local_exceptions
from .services import Google
from cannassaince.settings import GoogleSettings
from rest_framework.exceptions import AuthenticationFailed
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


from .models import CustomUser, UserProfile


class UserCreateSerializer(djoser_serializers.UserCreateSerializer):
    class Meta(djoser_serializers.UserCreateSerializer.Meta):
        model = CustomUser
        fields = ["id", "uuid","username", "email", "password"]

    # def create(self, validated_data):
    #     return CustomUser.objects.create(**validated_data)
    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print(data)
        data["message"] = "success"
        return data


class UsersSerializer(djoser_serializers.UserSerializer):
    class Meta(djoser_serializers.UserSerializer.Meta):
        model = CustomUser
        fields = [
            "id",
            "uuid",
            "email",
            "username",
            "is_active",
        ]


class LoginSerializer(TokenObtainPairSerializer):
    """Serializer for the login view to login a user with a customized response."""

    user_info = serializers.SerializerMethodField()

    @classmethod
    def get_token(cls, user: CustomUser):
        token = super().get_token(user)

        token["user_info"] = {
            "email": user.email,
            "username": user.username,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "is_active": user.is_active,
        }

        return token


class UserSocialProfileSerializer(serializers.ModelSerializer):
    """Serializer for adding extra info to the user profile."""

    user = UsersSerializer()
    facebook = serializers.URLField()
    apple = serializers.URLField()
    google = serializers.URLField()

    class Meta:
        model = UserProfile
        fields = ["user", "facebook", "apple", "google"]
        read_only_fields = ["user"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)

        if user_data is not None:
            for k, v in user_data.items():
                setattr(instance.user, k, v)

        instance.save()
        return instance

    def validate_facebook(self, validated_data):
        if urlparse(validated_data).netloc not in (
            "www.facebook.com",
            "facebook.com",
            "web.facebook.com",
        ):
            raise local_exceptions.InvalidFacebookLink
        return validated_data



class FacebookLoginSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
    state = serializers.CharField(required=False)


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    state = serializers.CharField(required=False)
