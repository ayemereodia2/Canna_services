import uuid
import random
import string
from django.db import models

from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from shared.models import SoftDeleteBaseModel, TimeAndUUIDStampedBaseModel

# Create your models here.


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
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    user_image = models.ImageField(upload_to=user_image, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            sliced_chars = self.email[:4]
            random_chars = "".join(
                random.choices("abcdefghijkmnoprsu" + string.digits, k=4)
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
        return f"{self.user.first_name} passcode"
