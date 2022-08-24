from django.db import models

from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=12, unique=True)
    phone_number = models.CharField(max_length=12)
    is_phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()
