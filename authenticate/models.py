import uuid
import random
import string
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from shared.models import SoftDeleteBaseModel, TimeAndUUIDStampedBaseModel

# Create your models here.


class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Please enter a valid email address"))

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("User must have an email address"))
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("is_staff must be true for admin user"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("is_superuser must be true for admin user"))

        user = self.create_user(email, first_name, last_name, password, **extra_fields)
        user.save(using=self._db)
        return user


def user_image(instance, filename):
    """Upload images to a the user's folder"""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"{instance.uuid}/avatar/{filename}"


class CustomUser(
    AbstractUser,
    SoftDeleteBaseModel,
    TimeAndUUIDStampedBaseModel,
):
    email = models.EmailField(
        verbose_name="Email", unique=True, blank=False, null=False
    )
    username = models.CharField(max_length=9, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    user_image = models.ImageField(upload_to=user_image, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            sliced_chars = self.email[:5]
            random_chars = "".join(
                random.choices("abcdefghijklmnoprsu" + string.digits, k=4)
            )
            self.username = sliced_chars + random_chars

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class UserProfile(SoftDeleteBaseModel, TimeAndUUIDStampedBaseModel):
    """
    User profile model for a user.
    """

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    facebook = models.URLField(blank=True, null=True)
    apple = models.URLField(blank=True, null=True)
    google = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.email


class OneTimePassword(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=4, unique=True, blank=True)

    def __str__(self):
        return f"{self.user.firstname} passcode"
