# Personal Assistant

Консольний персональний помічник: **книга контактів** (ім'я, адреса,
телефони, email, день народження) та **нотатки** з тегами. Навчальний
командний проєкт (Python, Neoversity/GoIT).

Дані зберігаються у `~/.personal_assistant/` і не втрачаються після
перезапуску. Змінна `PERSONAL_ASSISTANT_HOME` задає іншу теку (для тестів).
Працює лише на стандартній бібліотеці Python 3.10+.

## Встановлення

З Makefile (Linux, macOS; Windows через Git Bash або WSL):

```bash
make setup     # створює .venv і встановлює пакет з dev-залежностями
make start     # запуск
make test      # тести
make lint      # black --check + flake8
make format    # black
make doctor    # перевірка середовища
```

Без Makefile:

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python -m personal_assistant     # або: assistant
```

## Використання

Меню з командами показується один раз при старті. Далі працює цикл
команд до `exit`/`close`. Помилки вводу не завершують програму.

| Команда | Опис | Статус |
|---------|------|--------|
| `hello` | привітання | готово |
| `help` | список команд | готово |
| `exit`, `close` | зберегти і вийти | готово |
| contact commands (add, edit, delete, find, birthdays) | контакти | planned (#3) |
| note commands (add, find, edit, delete, tags) | нотатки | planned (#4) |
| interactive prompts, tables, command suggestions | CLI | planned (#5) |

Невідома команда: програма пропонує схожу (`difflib`) (planned, #5).

### Формати полів контакту

Некоректне значення не зберігається: помічник показує повідомлення
про помилку, а попереднє значення поля залишається без змін.

| Поле | Формат | Приклади, що приймаються |
|------|--------|--------------------------|
| Ім'я | непорожнє, до 50 символів; пробіли по краях обрізаються | `John`, `Олена` |
| Телефон | 10 цифр; пробіли, дефіси й дужки ігноруються; код `+380`/`380` замінюється на `0` | `0501234567`, `(050) 123-45-67`, `+380501234567` → `0501234567` |
| Email | `ім'я@домен.зона`, зберігається в нижньому регістрі | `john.doe@mail.com` |
| День народження | `DD.MM.YYYY`, не в майбутньому | `23.01.1990` |
| Адреса | непорожня, до 200 символів | `Kyiv, Khreshchatyk 1` |

## Структура проєкту

```
personal_assistant/
  __main__.py     python -m personal_assistant
  cli.py          цикл команд, реєстр команд, input_error   (#5)
  fields.py       Field, Name, Phone, Email, Birthday, Address (#2)
  exceptions.py   власні винятки                            (#2)
  contacts.py     Record, AddressBook                       (#3)
  notes.py        Note, NoteBook                            (#4)
  storage.py      збереження/завантаження (pickle)          (#1)
tests/            pytest; заглушки позначені skip
```

ООП: успадкування (`Field` -> `Name`, `Phone`, ...; `AddressBook` та
`NoteBook` від `UserDict`) і композиція (`Record` містить поля).

## Team & ownership

| # | Учасник | Роль | Відповідальність |
|---|---------|------|------------------|
| 1 | Учасник 1 | Team Lead | skeleton, `storage.py`, пакування, lint, code review |
| 2 | Учасник 2 | Developer | `fields.py`, `exceptions.py`, тести валідації |
| 3 | Учасник 3 | Developer | `contacts.py`: Record, AddressBook, пошук, дні народження |
| 4 | Учасник 4 | Developer | `notes.py`: Note, NoteBook, теги, пошук, сортування |
| 5 | Учасник 5 | Scrum Master | `cli.py`: цикл, диспетчер, `input_error`, help, таблиці, підказки команд |

Місця для роботи позначені `# TODO(owner #N)`.

## Git workflow

- Окрема гілка на задачу: `feature/<area>-<short>` (наприклад
  `feature/fields-phone`).
- PR у `main`, мінімум 1 review від Team Lead, без прямих push у `main`.
- Conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`.
- Перед PR: `make format lint test`. Деталі: [CONTRIBUTING.md](CONTRIBUTING.md).
