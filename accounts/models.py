import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from shared.models import SoftDeleteBaseModel, TimeAndUUIDStampedBaseModel
# Create your models here.


def user_image(instance, filename):
     """Upload images to a the user's folder"""
     ext = filename.split(".")[-1]
     filename = f"{uuid.uuid4()}.{ext}"
     return f"{instance.uuid}/avatar/{filename}"



class CustomUser(AbstractUser, SoftDeleteBaseModel, TimeAndUUIDStampedBaseModel,):
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    user_image = models.ImageField(upload_to=user_image, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email"]
