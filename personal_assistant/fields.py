"""Field classes with validation.

Owner: Participant 2 (Fields & validation).

All validation errors raise ``ValidationError`` with a user-friendly
message; ``input_error`` in cli.py shows it instead of crashing.

``Field`` is the base class and already works. Subclasses override
``validate`` which must return the normalised value or raise
``ValidationError``.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any

from personal_assistant.exceptions import ValidationError

NAME_MAX_LENGTH = 50
ADDRESS_MAX_LENGTH = 200
PHONE_DIGITS = 10
PHONE_PATTERN = re.compile(r"[0-9]{%d}" % PHONE_DIGITS)  # ASCII digits only
# Local part: letters, digits, "_%+-" and single dots (not at the edges).
# Domain: labels of letters/digits/hyphens, no hyphen at a label's edges.
EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9_%+-]+(\.[A-Za-z0-9_%+-]+)*"
    r"@([A-Za-z0-9]([A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}"
)
DATE_FORMAT = "%d.%m.%Y"
MIN_BIRTH_YEAR = 1900


class Field:
    """Base field: stores a value validated on every assignment."""

    def __init__(self, value: Any) -> None:
        self._value: Any = None
        self.value = value

    @property
    def value(self) -> Any:
        """Current (validated) value."""
        return self._value

    @value.setter
    def value(self, new_value: Any) -> None:
        if new_value is None:
            raise ValidationError(f"{type(self).__name__} is required.")
        self._value = self.validate(new_value)

    def validate(self, value: Any) -> Any:
        """Return the normalised value or raise ``ValidationError``.

        Subclasses override this hook. The base version accepts anything.
        """
        return value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Field):
            return type(self) is type(other) and self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash((type(self).__name__, self._value))


class Name(Field):
    """Contact name: required, non-empty, contains at least one letter."""

    def validate(self, value: Any) -> str:
        name = str(value).strip()
        if not name:
            raise ValidationError("Name cannot be empty.")
        if not any(char.isalpha() for char in name):
            raise ValidationError("Name must contain at least one letter.")
        if len(name) > NAME_MAX_LENGTH:
            raise ValidationError(
                f"Name is too long (max {NAME_MAX_LENGTH} characters)."
            )
        return name


class Phone(Field):
    """Phone number: digits, normalised (e.g. 10 digits).

    Accepts spaces, dashes, brackets and the Ukrainian country code:
    "(050) 123-45-67", "+380501234567" and "380501234567" all become
    "0501234567".
    """

    def validate(self, value: Any) -> str:
        digits = re.sub(r"[\s()\-]", "", str(value))
        if digits.startswith("+"):
            # Only the Ukrainian code is supported after "+".
            if not digits.startswith("+380"):
                raise ValidationError("Only +380 country code is supported.")
            digits = digits[1:]
        if digits.startswith("380") and len(digits) == PHONE_DIGITS + 2:
            digits = digits[2:]  # "380501234567" -> "0501234567"
        if not PHONE_PATTERN.fullmatch(digits):
            raise ValidationError(
                f"Phone must contain exactly {PHONE_DIGITS} digits, e.g. 0501234567."
            )
        return digits


class Email(Field):
    """E-mail address."""

    def validate(self, value: Any) -> str:
        email = str(value).strip()
        if not EMAIL_PATTERN.fullmatch(email):
            raise ValidationError("Invalid e-mail. Example: name@example.com")
        return email.lower()


class Birthday(Field):
    """Birthday in DD.MM.YYYY format, from 1900 and not in the future.

    ``value`` holds a ``datetime.date``.
    """

    def validate(self, value: Any) -> Any:
        if isinstance(value, datetime):
            birthday = value.date()
        elif isinstance(value, date):
            birthday = value
        else:
            try:
                birthday = datetime.strptime(str(value).strip(), DATE_FORMAT).date()
            except ValueError as err:
                raise ValidationError(
                    "Invalid date. Use DD.MM.YYYY, e.g. 23.01.1990."
                ) from err
        if birthday > date.today():
            raise ValidationError("Birthday cannot be in the future.")
        if birthday.year < MIN_BIRTH_YEAR:
            raise ValidationError(f"Birthday year must be {MIN_BIRTH_YEAR} or later.")
        return birthday

    def __str__(self) -> str:
        return self._value.strftime(DATE_FORMAT)


class Address(Field):
    """Postal address: free text, non-empty, length limit."""

    def validate(self, value: Any) -> str:
        address = str(value).strip()
        if not address:
            raise ValidationError("Address cannot be empty.")
        if len(address) > ADDRESS_MAX_LENGTH:
            raise ValidationError(
                f"Address is too long (max {ADDRESS_MAX_LENGTH} characters)."
            )
        return address
