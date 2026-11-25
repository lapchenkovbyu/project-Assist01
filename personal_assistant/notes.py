"""Notes with tags: ``Note`` and ``NoteBook``.

Owner: Participant 4 (Notes & tags).
"""

from __future__ import annotations

from collections import UserDict
from datetime import datetime


class Note:
    """One note: title, text, tags, creation time."""

    def __init__(self, title: str, text: str, tags: list[str] | None = None):
        self.title: str = title
        self.text: str = text
        self.tags: list[str] = list(tags or [])
        self.created_at: datetime = datetime.now()
        # TODO(owner #4): validate title/text/tags (non-empty, tag format)

    def add_tag(self, tag: str) -> None:
        """Add a tag (no duplicates, normalised to lower case)."""
        # TODO(owner #4)
        raise NotImplementedError

    def remove_tag(self, tag: str) -> None:
        """Remove a tag; raise ``NotFoundError`` if missing."""
        # TODO(owner #4)
        raise NotImplementedError

    def edit(self, title: str | None = None, text: str | None = None) -> None:
        """Change title and/or text."""
        # TODO(owner #4)
        raise NotImplementedError

    def __str__(self) -> str:
        # TODO(owner #4): readable representation
        return f"{self.title}: {self.text}"


class NoteBook(UserDict):
    """Collection of notes keyed by integer id (1, 2, 3...)."""

    def add_note(self, note: Note) -> int:
        """Store a note and return its new id."""
        # TODO(owner #4)
        raise NotImplementedError

    def get_note(self, note_id: int) -> Note:
        """Lookup by id; raise ``NotFoundError`` if missing."""
        # TODO(owner #4)
        raise NotImplementedError

    def search_text(self, query: str) -> list[tuple[int, Note]]:
        """Case-insensitive search in title and text."""
        # TODO(owner #4)
        raise NotImplementedError

    def edit_note(
        self, note_id: int, title: str | None = None, text: str | None = None
    ) -> None:
        """Edit a note by id."""
        # TODO(owner #4)
        raise NotImplementedError

    def delete_note(self, note_id: int) -> None:
        """Delete a note by id."""
        # TODO(owner #4)
        raise NotImplementedError

    def add_tag(self, note_id: int, tag: str) -> None:
        """Add a tag to a note."""
        # TODO(owner #4)
        raise NotImplementedError

    def remove_tag(self, note_id: int, tag: str) -> None:
        """Remove a tag from a note."""
        # TODO(owner #4)
        raise NotImplementedError

    def search_by_tag(self, tag: str) -> list[tuple[int, Note]]:
        """Notes that have ``tag``."""
        # TODO(owner #4)
        raise NotImplementedError

    def sorted_by_tag(self) -> list[tuple[int, Note]]:
        """All notes sorted by their tags."""
        # TODO(owner #4)
        raise NotImplementedError
