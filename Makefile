# Single setup/run entry point. Linux, macOS, Windows (Git Bash or WSL).
ifeq ($(OS),Windows_NT)
	BIN := .venv/Scripts
	SYS_PY ?= python
else
	BIN := .venv/bin
	SYS_PY ?= python3
endif
PY := $(BIN)/python

.PHONY: setup start test lint format doctor clean

setup:
	$(SYS_PY) -m venv .venv
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -e ".[dev]"

start:
	$(PY) -m personal_assistant

test:
	$(PY) -m pytest -v

lint:
	$(PY) -m black --check .
	$(PY) -m flake8

format:
	$(PY) -m black .

doctor:
	@$(SYS_PY) --version
	@test -x $(PY) && echo "venv: ok ($(BIN))" || echo "venv: missing, run make setup"
	@test -x $(PY) && $(PY) -c "import personal_assistant; print(\"package: ok\")" || true

clean:
	rm -rf build dist *.egg-info .pytest_cache
	find . -name __pycache__ -type d -not -path "./.venv/*" -prune -exec rm -rf {} +
