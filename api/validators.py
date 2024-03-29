from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible

from rest_framework.exceptions import ValidationError

from typing import AnyStr
import re


def password_validator(password: str) -> str:
    """
    Validate the strength of a password.

    Return Type -> str:
    # str: return password string after validate.
    """

    min_length: int = 8
    max_length: int = 20
    re_pattern: AnyStr = (
        r"(?=^.{8,}$)(?=.*\d)(?=.*[!@#$%^&*]+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$"
    )

    if not (min_length <= len(password) <= max_length):
        raise ValidationError(_("Password must between 8 to 20 character."))

    if not re.fullmatch(re_pattern, password):
        raise ValidationError(_("Password must be strong."))

    return password


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"^[a-zA-Z0-9_-]+$"
    message = _(
        "Enter a valid username. It contain only letters, "
        "numbers, and /-/_ characters."
    )
    flags = 0
