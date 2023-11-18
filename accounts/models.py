import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from shared.models import SoftDeleteBaseModel, TimeAndUUIDStampedBaseModel
# Create your models here.


def user_image(instance, filename):
     """Upload images to a the user's folder"""
     ext = filename.split(".")[-1]
     filename = f"{uuid.uuid4()}.{ext}"
     return f"{instance.uuid}/avatar/{filename}"



class CustomUser(AbstractUser, SoftDeleteBaseModel, TimeAndUUIDStampedBaseModel,):
    email = models.EmailField(unique=True, blank=False, null=False)
    otp = models.CharField(max_length=4, null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    user_image = models.ImageField(upload_to=user_image, blank=True, null=True)

    USERNAME_FIELD = "email"


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