from rest_framework import serializers
from djoser import serializers as djoser_serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import IntegrityError, transaction
from djoser.conf import settings
from rest_framework.response import Response
from rest_framework import status


from .models import CustomUser


class UserCreateSerializer(djoser_serializers.UserCreateSerializer):
    class Meta(djoser_serializers.UserCreateSerializer.Meta):
        model = CustomUser
        fields = ["id", "uuid", "first_name", "last_name", "email", "password"]

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

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
            "first_name",
            "last_name",
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
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "is_active": user.is_active,
        }

        return token
