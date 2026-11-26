"""Address book: ``Record`` and ``AddressBook``.

Owner: Participant 3 (Contacts).

``Record`` is a composition of field objects (Name, Phone, Email,
Birthday, Address). ``AddressBook`` is a ``UserDict`` keyed by name.
"""

from __future__ import annotations

from collections import UserDict
from datetime import date, timedelta
from typing import Optional

from personal_assistant.exceptions import DuplicateError, NotFoundError
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
        phone_obj = Phone(phone)

        if phone_obj in self.phones:
            raise DuplicateError(f"Phone {phone_obj} already exists.")

        self.phones.append(phone_obj)

    def edit_phone(self, old: str, new: str) -> None:
        """Replace ``old`` phone with ``new``."""
        old_phone = Phone(old)
        new_phone = Phone(new)

        for index, phone in enumerate(self.phones):
            if phone == old_phone:
                if new_phone in self.phones and new_phone != phone:
                    raise DuplicateError(
                        f"Phone {new_phone} already exists."
                    )

                self.phones[index] = new_phone
                return

        raise NotFoundError(f"Phone {old_phone} not found.")

    def remove_phone(self, phone: str) -> None:
        """Remove a phone."""
        phone_obj = Phone(phone)

        for existing_phone in self.phones:
            if existing_phone == phone_obj:
                self.phones.remove(existing_phone)
                return

        raise NotFoundError(f"Phone {phone_obj} not found.")

    def set_email(self, email: str) -> None:
        """Set or replace the e-mail."""
        self.email = Email(email)

    def remove_email(self) -> None:
        """Remove the e-mail."""
        self.email = None

    def set_address(self, address: str) -> None:
        """Set or replace the address."""
        self.address = Address(address)

    def remove_address(self) -> None:
        """Remove the address."""
        self.address = None

    def set_birthday(self, birthday: str) -> None:
        """Set or replace the birthday (DD.MM.YYYY)."""
        self.birthday = Birthday(birthday)

    def remove_birthday(self) -> None:
        """Remove the birthday."""
        self.birthday = None

    def days_to_birthday(self) -> Optional[int]:
        """Days until the next birthday, or None if not set."""
        if self.birthday is None:
            return None

        today = date.today()
        birthday = self.birthday.value

        try:
            next_birthday = birthday.replace(year=today.year)
        except ValueError:
            # February 29 in a non-leap year.
            next_birthday = date(today.year, 2, 28)

        if next_birthday < today:
            try:
                next_birthday = birthday.replace(year=today.year + 1)
            except ValueError:
                next_birthday = date(today.year + 1, 2, 28)

        return (next_birthday - today).days

    def __str__(self) -> str:
        """Readable one-record representation."""
        phones = ", ".join(str(phone) for phone in self.phones)

        result = f"Contact name: {self.name}"

        if phones:
            result += f", phones: {phones}"

        if self.email is not None:
            result += f", email: {self.email}"

        if self.address is not None:
            result += f", address: {self.address}"

        if self.birthday is not None:
            result += f", birthday: {self.birthday}"

        return result


class AddressBook(UserDict):
    """Collection of records keyed by ``Name.value``."""

    def add_record(self, record: Record) -> None:
        """Add a record; raise ``DuplicateError`` if the name exists."""
        key = record.name.value

        if key in self.data:
            raise DuplicateError(f"Contact '{key}' already exists.")

        self.data[key] = record

    def find(self, query: str) -> list[Record]:
        """Partial match on name, phone or e-mail (case-insensitive)."""
        query = str(query).strip().casefold()

        if not query:
            return []

        result = []

        for record in self.data.values():
            if query in str(record.name).casefold():
                result.append(record)
                continue

            if any(query in str(phone).casefold() for phone in record.phones):
                result.append(record)
                continue

            if record.email is not None:
                if query in str(record.email).casefold():
                    result.append(record)

        return result

    def get_record(self, name: str) -> Record:
        """Exact lookup by name; raise ``NotFoundError`` if missing."""
        if name in self.data:
            return self.data[name]

        # Case-insensitive exact search.
        name_lower = name.strip().casefold()

        for key, record in self.data.items():
            if key.casefold() == name_lower:
                return record

        raise NotFoundError(f"Contact '{name}' not found.")

    def delete(self, name: str) -> None:
        """Delete a record; raise ``NotFoundError`` if missing."""
        record = self.get_record(name)
        del self.data[record.name.value]

    def upcoming_birthdays(self, days: int) -> list[Record]:
        """Records with a birthday within the next ``days`` days."""
        if days < 0:
            raise ValueError("days cannot be negative.")

        result = []

        for record in self.data.values():
            days_to_birthday = record.days_to_birthday()

            if days_to_birthday is not None and days_to_birthday <= days:
                result.append(record)

        result.sort(
            key=lambda record: (
                record.days_to_birthday()
                if record.days_to_birthday() is not None
                else 999999
            )
        )

        return result