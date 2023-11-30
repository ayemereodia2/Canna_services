from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser

"""
Create and update custom user form on admin
"""


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", 'first_name', 'last_name',"created_at", "updated_at")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "username", "created_at", "updated_at")
