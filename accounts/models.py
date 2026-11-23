
from django.contrib.auth.models import AbstractUser  # type: ignore[import-untyped]
from django.db import models  # type: ignore[import-untyped]


class CustomUser(AbstractUser):
    """Custom user model with additional profile information."""

    age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
    )

    bio = models.TextField(
        max_length=500,
        blank=True,
    )

    def __str__(self):
        return self.username

