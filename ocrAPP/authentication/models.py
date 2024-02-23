from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField("Phone Number", max_length=15)
    address = models.CharField("Address", max_length=255)
    gender = models.CharField(max_length=10)

    class Meta:
        db_table = 'custom_auth_user'