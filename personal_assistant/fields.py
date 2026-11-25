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
PHONE_DIGITS = 10
EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w-]+(\.[\w-]+)*\.[A-Za-z]{2,}")
DATE_FORMAT = "%d.%m.%Y"


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
    """Contact name: required, non-empty."""

    def validate(self, value: Any) -> str:
        name = str(value).strip()
        if not name:
            raise ValidationError("Name cannot be empty.")
        if len(name) > NAME_MAX_LENGTH:
            raise ValidationError(
                f"Name is too long (max {NAME_MAX_LENGTH} characters)."
            )
        return name


class Phone(Field):
    """Phone number: digits, normalised (e.g. 10 digits)."""

    def validate(self, value: Any) -> str:
        # Allow common separators like spaces, dashes, brackets: "(050) 123-45-67".
        digits = re.sub(r"[\s()\-]", "", str(value))
        if not digits.isdigit() or len(digits) != PHONE_DIGITS:
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
    """Birthday in DD.MM.YYYY format, not in the future.

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
        return birthday

    def __str__(self) -> str:
        return self._value.strftime(DATE_FORMAT)


class Address(Field):
    """Postal address: free text, non-empty."""

    def validate(self, value: Any) -> str:
        address = str(value).strip()
        if not address:
            raise ValidationError("Address cannot be empty.")
        return address
