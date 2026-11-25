# Contributing

1. `make setup`, then `pre-commit install`.
2. Branch from `main`: `feature/<area>-<short>` (areas: fields, contacts,
   notes, cli, infra), e.g. `feature/contacts-find`.
3. Commit with conventional messages: `feat:`, `fix:`, `docs:`, `test:`,
   `refactor:`, `chore:`.
4. Before a PR: `make format`, `make lint`, `make test`.
5. Open a PR into `main` using the template. At least one review from the
   Team Lead is required. No direct pushes to `main`.
6. Work only in your own module to avoid merge conflicts; ask the module
   owner when you need a change elsewhere. Register CLI commands with
   `@command` in `cli.py` (or a module imported from it).

Style: PEP 8, black (88), flake8, type hints, docstrings.
