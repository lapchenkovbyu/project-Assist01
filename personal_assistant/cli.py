"""Command line interface: loop, dispatcher, command registry.

Owner: Participant 5 (CLI + Scrum Master). Skeleton by Team Lead.

How to add a command: write a function ``(args, ctx) -> str`` and
decorate it with ``@command("name", "usage text")``. Wrap it with
``@input_error`` so bad input returns a message instead of crashing.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass, field
from typing import Callable

from personal_assistant import storage
from personal_assistant.contacts import AddressBook
from personal_assistant.exceptions import AssistantError
from personal_assistant.notes import NoteBook

PROMPT = "> "


@dataclass
class Context:
    """Shared state passed to every handler."""

    book: AddressBook = field(default_factory=AddressBook)
    notes: NoteBook = field(default_factory=NoteBook)


Handler = Callable[[list[str], Context], str]

# name -> (handler, usage). Teammates register commands via @command.
COMMANDS: dict[str, tuple[Handler, str]] = {}
EXIT_COMMANDS = ("exit", "close")


def command(name: str, usage: str = "") -> Callable[[Handler], Handler]:
    """Register a handler in ``COMMANDS``."""

    def decorator(func: Handler) -> Handler:
        COMMANDS[name] = (func, usage or name)
        return func

    return decorator


def input_error(func: Handler) -> Handler:
    """Turn expected errors into messages; the program must not crash."""

    @functools.wraps(func)
    def wrapper(args: list[str], ctx: Context) -> str:
        try:
            return func(args, ctx)
        except AssistantError as err:
            return f"Error: {err}"
        except ValueError as err:
            return f"Invalid value: {err}"
        except IndexError:
            return "Not enough arguments. Type 'help' for usage."
        except KeyError as err:
            return f"Not found: {err}"
        except NotImplementedError:
            return "This command is not implemented yet."

    return wrapper


def parse_input(line: str) -> tuple[str, list[str]]:
    """Split a line into ``(command, args)``; command is lower case."""
    parts = line.strip().split()
    if not parts:
        return "", []
    return parts[0].lower(), parts[1:]


def suggest_command(name: str) -> str | None:
    """Return the closest known command or None."""
    # TODO(owner #5): difflib.get_close_matches over COMMANDS + EXIT_COMMANDS
    return None


def help_text() -> str:
    """Command list (also printed once at startup)."""
    lines = ["Commands:"]
    for _, usage in sorted((n, u) for n, (_, u) in COMMANDS.items()):
        lines.append(f"  {usage}")
    lines.append("  exit | close - save and quit")
    return "\n".join(lines)


@command("hello", "hello - greeting")
@input_error
def cmd_hello(args: list[str], ctx: Context) -> str:
    return "How can I help you?"


@command("help", "help - show commands")
@input_error
def cmd_help(args: list[str], ctx: Context) -> str:
    return help_text()


# TODO(owner #3): contact commands (add, edit, delete, find, birthdays...)
# TODO(owner #4): note commands (note-add, note-find, tag-add, ...)
# TODO(owner #5): table output, interactive prompts, suggestions


def dispatch(line: str, ctx: Context) -> str:
    """Run one input line and return the reply text."""
    name, args = parse_input(line)
    if not name:
        return ""
    entry = COMMANDS.get(name)
    if entry is None:
        hint = suggest_command(name)
        extra = f" Did you mean '{hint}'?" if hint else ""
        return f"Unknown command '{name}'.{extra} Type 'help'."
    return entry[0](args, ctx)


def main() -> None:
    """Run the interactive loop until exit."""
    ctx = Context(book=storage.load_address_book(), notes=storage.load_notes())
    print("Welcome to the personal assistant!")
    print(help_text())
    try:
        while True:
            try:
                line = input(PROMPT)
            except EOFError:
                break
            name, _ = parse_input(line)
            if name in EXIT_COMMANDS:
                break
            reply = dispatch(line, ctx)
            if reply:
                print(reply)
    except KeyboardInterrupt:
        print()
    finally:
        try:
            storage.save_address_book(ctx.book)
            storage.save_notes(ctx.notes)
        except OSError as err:
            print(f"Could not save data: {err}")
    print("Good bye!")


if __name__ == "__main__":
    main()
