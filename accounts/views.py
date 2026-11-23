
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import CustomUserCreationForm, UserProfileForm
from .models import CustomUser


class SignUpView(CreateView):
    """Register a new user."""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Allow logged-in users to update their profile."""

    model = CustomUser
    form_class = UserProfileForm
    template_name = "registration/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        """Return the currently authenticated user."""
        return self.request.user

    def form_valid(self, form):
        """Display a confirmation after a successful update."""

        messages.success(
            self.request,
            "Your profile has been updated successfully!",
        )

        return super().form_valid(form)

