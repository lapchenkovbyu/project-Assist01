import subprocess
import sys

from personal_assistant.cli import Context, dispatch, input_error
from personal_assistant.exceptions import ValidationError


def test_hello():
    assert "help" in dispatch("hello", Context()).lower()


def test_unknown_command():
    assert "Unknown command" in dispatch("foo", Context())


def test_empty_line():
    assert dispatch("   ", Context()) == ""


def test_input_error_catches():
    @input_error
    def boom(args, ctx):
        raise ValidationError("bad")

    assert "bad" in boom([], Context())


def test_end_to_end(data_dir):
    result = subprocess.run(
        [sys.executable, "-m", "personal_assistant"],
        input="hello\nfoo\nexit\n",
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    assert "Unknown command" in result.stdout
    assert result.stdout.count("Commands:") == 1
    assert (data_dir / "address_book.pkl").exists()


def test_eof_exits_cleanly(data_dir):
    result = subprocess.run(
        [sys.executable, "-m", "personal_assistant"],
        input="",
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
