"""Field classes with validation.

Owner: Participant 2 (Fields & validation).

``Field`` is the base class and already works. Subclasses override
``validate`` which must return the normalised value or raise
``ValidationError``.
"""

from __future__ import annotations

from typing import Any

from personal_assistant.exceptions import ValidationError  # noqa: F401


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
        # TODO(owner #2): implement (strip, non-empty, max length)
        raise NotImplementedError


class Phone(Field):
    """Phone number: digits, normalised (e.g. 10 digits)."""

    def validate(self, value: Any) -> str:
        # TODO(owner #2): implement
        raise NotImplementedError


class Email(Field):
    """E-mail address."""

    def validate(self, value: Any) -> str:
        # TODO(owner #2): implement (regex)
        raise NotImplementedError


class Birthday(Field):
    """Birthday in DD.MM.YYYY format, not in the future.

    ``value`` holds a ``datetime.date``.
    """

    def validate(self, value: Any) -> Any:
        # TODO(owner #2): implement (strptime, not in future)
        raise NotImplementedError


class Address(Field):
    """Postal address: free text, non-empty."""

    def validate(self, value: Any) -> str:
        # TODO(owner #2): implement
        raise NotImplementedError
