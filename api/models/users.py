from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from api.manager import UserManager
from api.utils import generate_unique_token
from .base import BaseModel

from datetime import datetime, timedelta


class Users(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    A Custom User model class extending AbstractBaseUser
    and PermissionsMixin.

    Note:
    The purpose of this class is to allow future changes.
    """

    username: models.CharField = models.CharField(
        _("Username"), max_length=50, unique=True, null=False, blank=False
    )
    email: models.EmailField = models.EmailField(
        _("Email Address"), max_length=255, unique=True, null=False, blank=False
    )
    security_token: models.CharField = models.CharField(
        _("Security Token"), max_length=64, default=generate_unique_token
    )
    new_email: models.EmailField = models.EmailField(
        "New Email Address", null=True, blank=True
    )

    is_active: models.BooleanField = models.BooleanField(_("Active"), default=False)
    is_staff: models.BooleanField = models.BooleanField(_("Staff"), default=False)
    is_sent: models.DateTimeField = models.DateTimeField(
        _("Token Send"), default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email", "password"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ("-created_at",)

    def send_confirmation_mail(self) -> None:
        """
        Send a confirmation email with a link for user
        account activation.
        """
        self.set_security_token

        confirm_url: str = "{}{}".format(
            settings.CLIENT_SITE_URL,
            reverse("confirm_account", kwargs={"token": self.security_token}),
        )
        print(confirm_url)

        message: str = f"""
        Click the following link to confirm your account. \n{confirm_url}
        """

        send_mail(
            "Confirm Your Account",
            message=message,
            from_email=settings.EMAIL_FROM,
            recipient_list=[self.email],
            fail_silently=False,
        )

    @property
    def set_security_token(self) -> None:
        """
        Set url token string for account verification and
        reset email address.
        """
        self.security_token: str = generate_unique_token()
        self.is_sent = timezone.now()

    @property
    def is_token_expired(self) -> bool:
        """
        Check if the security token has expired.
        """
        expiry_time = self.is_sent + timedelta(minutes=30)
        current_time = timezone.now()
        return current_time > expiry_time

    def __str__(self):
        return "User >> {}".format(self.username)
