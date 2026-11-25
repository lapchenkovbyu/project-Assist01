"""Address book: ``Record`` and ``AddressBook``.

Owner: Participant 3 (Contacts).

``Record`` is a composition of field objects (Name, Phone, Email,
Birthday, Address). ``AddressBook`` is a ``UserDict`` keyed by name.
"""

from __future__ import annotations

from collections import UserDict
from typing import Optional

from personal_assistant.fields import Address, Birthday, Email, Name, Phone


class Record:
    """One contact."""

    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: list[Phone] = []
        self.email: Optional[Email] = None
        self.address: Optional[Address] = None
        self.birthday: Optional[Birthday] = None

    def add_phone(self, phone: str) -> None:
        """Validate and add a phone."""
        # TODO(owner #3)
        raise NotImplementedError

    def edit_phone(self, old: str, new: str) -> None:
        """Replace ``old`` phone with ``new``."""
        # TODO(owner #3)
        raise NotImplementedError

    def remove_phone(self, phone: str) -> None:
        """Remove a phone."""
        # TODO(owner #3)
        raise NotImplementedError

    def set_email(self, email: str) -> None:
        """Set or replace the e-mail."""
        # TODO(owner #3)
        raise NotImplementedError

    def remove_email(self) -> None:
        """Remove the e-mail."""
        # TODO(owner #3)
        raise NotImplementedError

    def set_address(self, address: str) -> None:
        """Set or replace the address."""
        # TODO(owner #3)
        raise NotImplementedError

    def remove_address(self) -> None:
        """Remove the address."""
        # TODO(owner #3)
        raise NotImplementedError

    def set_birthday(self, birthday: str) -> None:
        """Set or replace the birthday (DD.MM.YYYY)."""
        # TODO(owner #3)
        raise NotImplementedError

    def remove_birthday(self) -> None:
        """Remove the birthday."""
        # TODO(owner #3)
        raise NotImplementedError

    def days_to_birthday(self) -> Optional[int]:
        """Days until the next birthday, or None if not set."""
        # TODO(owner #3)
        raise NotImplementedError

    def __str__(self) -> str:
        # TODO(owner #3): readable one-record representation
        return f"Contact name: {self.name}"


class AddressBook(UserDict):
    """Collection of records keyed by ``Name.value``."""

    def add_record(self, record: Record) -> None:
        """Add a record; raise ``DuplicateError`` if the name exists."""
        # TODO(owner #3)
        raise NotImplementedError

    def find(self, query: str) -> list[Record]:
        """Partial match on name, phone or e-mail (case-insensitive)."""
        # TODO(owner #3)
        raise NotImplementedError

    def get_record(self, name: str) -> Record:
        """Exact lookup by name; raise ``NotFoundError`` if missing."""
        # TODO(owner #3)
        raise NotImplementedError

    def delete(self, name: str) -> None:
        """Delete a record; raise ``NotFoundError`` if missing."""
        # TODO(owner #3)
        raise NotImplementedError

    def upcoming_birthdays(self, days: int) -> list[Record]:
        """Records with a birthday within the next ``days`` days."""
        # TODO(owner #3)
        raise NotImplementedError
