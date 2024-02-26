from .register import (
    UserRegisterView,
    UserAccountConfirmView,
)
from .login import UserLoginView
from .logout import UserLogoutView
from .change_password import ChangePasswordView
from .reset_password import (
    ResetPasswordView,
    ResetPasswordConfirmView,
)
from .reset_email import (
    ResetEmailView,
    ResetEmailConfirmView,
)
from .user_detail import UserDetailView

__all__ = [
    "UserRegisterView",
    "UserLoginView",
    "UserLogoutView",
    "UserAccountConfirmView",
    "ResetPasswordView",
    "ResetPasswordConfirmView",
    "ChangePasswordView",
    "ResetEmailView",
    "ResetEmailConfirmView",
    "UserDetailView",
]
