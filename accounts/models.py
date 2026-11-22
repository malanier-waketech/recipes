from django.contrib.auth.models import AbstractUser  # type: ignore[import-untyped]
from django.db import models  # type: ignore[import-untyped]


# Create your models here.
class CustomUser(AbstractUser):
    # Add any additional fields you need for your custom user model
    age = models.PositiveIntegerField(null=True, blank=True)
