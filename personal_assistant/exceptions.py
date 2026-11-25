"""Custom exceptions.

Owner: Participant 2 (Fields & validation).
Add new exception types here; ``input_error`` in cli.py catches
``AssistantError`` and turns it into a user-friendly message.
"""


class AssistantError(Exception):
    """Base class for all application errors."""


class ValidationError(AssistantError, ValueError):
    """A field value has an invalid format."""


class NotFoundError(AssistantError):
    """A contact, note, phone, tag, etc. was not found."""


class DuplicateError(AssistantError):
    """An entity with the same key already exists."""
