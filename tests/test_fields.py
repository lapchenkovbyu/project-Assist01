"""Tests for field validation (Name, Phone, Email, Birthday, Address)."""

from datetime import date, timedelta

import pytest

from personal_assistant.exceptions import AssistantError, ValidationError
from personal_assistant.fields import Address, Birthday, Email, Name, Phone

# ---------- Name ----------


def test_name_is_stripped():
    assert Name("  John ").value == "John"


@pytest.mark.parametrize("bad", ["", "   ", "x" * 51])
def test_name_invalid(bad):
    with pytest.raises(ValidationError):
        Name(bad)


# ---------- Phone ----------


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("0501234567", "0501234567"),
        ("050 123 45 67", "0501234567"),
        ("(050)123-45-67", "0501234567"),
        ("+380501234567", "0501234567"),
        ("380501234567", "0501234567"),
        ("+38 (050) 123-45-67", "0501234567"),
    ],
)
def test_phone_valid_and_normalised(raw, expected):
    assert Phone(raw).value == expected


@pytest.mark.parametrize(
    "bad", ["", "12345", "050123456789", "05012abcde", "+38050123456", "+1234567890"]
)
def test_phone_invalid(bad):
    with pytest.raises(ValidationError):
        Phone(bad)


def test_phone_bad_update_keeps_old_value():
    phone = Phone("0501234567")
    with pytest.raises(ValidationError):
        phone.value = "123"
    assert phone.value == "0501234567"


# ---------- Email ----------


@pytest.mark.parametrize("good", ["john@mail.com", "John.Doe+work@mail.co.uk"])
def test_email_valid(good):
    assert Email(good).value == good.lower()


@pytest.mark.parametrize(
    "bad", ["", "john", "john@", "@mail.com", "john@mail", "john mail@x.com"]
)
def test_email_invalid(bad):
    with pytest.raises(ValidationError):
        Email(bad)


# ---------- Birthday ----------


def test_birthday_valid():
    bday = Birthday("23.01.1990")
    assert bday.value == date(1990, 1, 23)
    assert str(bday) == "23.01.1990"


def test_birthday_accepts_date_object():
    assert Birthday(date(2000, 5, 1)).value == date(2000, 5, 1)


@pytest.mark.parametrize("bad", ["1990-01-23", "31.02.1990", "abc", ""])
def test_birthday_invalid_format(bad):
    with pytest.raises(ValidationError):
        Birthday(bad)


def test_birthday_not_in_future():
    tomorrow = (date.today() + timedelta(days=1)).strftime("%d.%m.%Y")
    with pytest.raises(ValidationError):
        Birthday(tomorrow)


# ---------- Address ----------


def test_address_valid():
    assert Address(" Kyiv, Khreshchatyk 1 ").value == "Kyiv, Khreshchatyk 1"


@pytest.mark.parametrize("bad", ["", "   ", "x" * 201])
def test_address_invalid(bad):
    with pytest.raises(ValidationError):
        Address(bad)


# ---------- Common ----------


@pytest.mark.parametrize(
    "cls, bad", [(Name, ""), (Phone, "1"), (Email, "x"), (Birthday, "x"), (Address, "")]
)
def test_errors_are_assistant_errors(cls, bad):
    """cli.input_error catches AssistantError, so the app never crashes."""
    with pytest.raises(AssistantError):
        cls(bad)
