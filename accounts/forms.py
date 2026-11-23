
from django import forms
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
)

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Form for registering new users."""

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    """Form for managing users in Django Admin."""

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class UserProfileForm(forms.ModelForm):
    """Allow users to update their profile information."""

    class Meta:
        model = CustomUser

        fields = (
            "first_name",
            "last_name",
            "email",
            "age",
            "avatar",
            "bio",
        )

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "age": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "avatar": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Tell us about your cooking interests...",
                }
            ),
        }
