from personal_assistant import storage
from personal_assistant.contacts import AddressBook
from personal_assistant.fields import Field
from personal_assistant.notes import NoteBook


def test_load_missing_returns_empty():
    assert storage.load_address_book() == {}
    assert storage.load_notes() == {}


def test_round_trip(data_dir):
    book = AddressBook()
    book["alice"] = Field("alice")
    notes = NoteBook()
    notes[1] = "placeholder"
    storage.save_address_book(book)
    storage.save_notes(notes)
    assert (data_dir / storage.ADDRESS_BOOK_FILE).exists()
    assert storage.load_address_book()["alice"] == Field("alice")
    assert storage.load_notes()[1] == "placeholder"


def test_corrupt_file_starts_empty(data_dir):
    (data_dir / storage.ADDRESS_BOOK_FILE).write_bytes(b"not a pickle")
    assert isinstance(storage.load_address_book(), AddressBook)
    assert storage.load_address_book() == {}
    assert (data_dir / (storage.ADDRESS_BOOK_FILE + ".corrupt")).exists()


def test_wrong_type_starts_empty(data_dir):
    storage._save({"a": 1}, storage.NOTES_FILE)
    assert storage.load_notes() == {}


def test_data_dir_created(tmp_path, monkeypatch):
    target = tmp_path / "nested" / "dir"
    monkeypatch.setenv("PERSONAL_ASSISTANT_HOME", str(target))
    assert storage.get_data_dir() == target
    assert target.is_dir()
