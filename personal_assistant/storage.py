"""Persistence of the address book and notes (pickle).

Owner: Team Lead (Participant 1).

Data lives in ``~/.personal_assistant/`` (override with the
``PERSONAL_ASSISTANT_HOME`` environment variable, e.g. in tests).
A missing or corrupt file never crashes the app: it starts empty.
"""

from __future__ import annotations

import os
import pickle
from pathlib import Path
from typing import Any, Callable

from personal_assistant.contacts import AddressBook
from personal_assistant.notes import NoteBook

ENV_HOME = "PERSONAL_ASSISTANT_HOME"
ADDRESS_BOOK_FILE = "address_book.pkl"
NOTES_FILE = "notes.pkl"


def get_data_dir() -> Path:
    """Return the data directory, creating it if needed."""
    override = os.environ.get(ENV_HOME)
    path = Path(override) if override else Path.home() / ".personal_assistant"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _save(obj: Any, filename: str) -> None:
    target = get_data_dir() / filename
    tmp = target.with_suffix(target.suffix + ".tmp")
    with open(tmp, "wb") as fh:
        pickle.dump(obj, fh)
    os.replace(tmp, target)


def _load(filename: str, factory: Callable[[], Any], expected: type) -> Any:
    path = get_data_dir() / filename
    if not path.exists():
        return factory()
    try:
        with open(path, "rb") as fh:
            obj = pickle.load(fh)
    except Exception:  # corrupt, truncated or incompatible file
        _quarantine(path)
        return factory()
    if not isinstance(obj, expected):
        _quarantine(path)
        return factory()
    return obj


def _quarantine(path: Path) -> None:
    """Keep a broken file as ``*.corrupt`` so data is not silently lost."""
    try:
        os.replace(path, path.with_suffix(path.suffix + ".corrupt"))
    except OSError:
        pass


def save_address_book(book: AddressBook) -> None:
    """Write the address book to disk."""
    _save(book, ADDRESS_BOOK_FILE)


def load_address_book() -> AddressBook:
    """Read the address book, or return an empty one."""
    return _load(ADDRESS_BOOK_FILE, AddressBook, AddressBook)


def save_notes(notebook: NoteBook) -> None:
    """Write the notebook to disk."""
    _save(notebook, NOTES_FILE)


def load_notes() -> NoteBook:
    """Read the notebook, or return an empty one."""
    return _load(NOTES_FILE, NoteBook, NoteBook)
