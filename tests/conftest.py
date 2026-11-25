import pytest


@pytest.fixture(autouse=True)
def data_dir(tmp_path, monkeypatch):
    """Isolate every test from the real ~/.personal_assistant."""
    monkeypatch.setenv("PERSONAL_ASSISTANT_HOME", str(tmp_path))
    return tmp_path
