"""Shared pytest fixtures.

Sets up an isolated, temporary SQLite database *before* importing the
application, so tests never touch the developer's real ``data/ai_powered_crm.db``
file. AI features are also disabled by default (no API key) so the test
suite runs deterministically without any network calls.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# IMPORTANT: environment variables must be set before `app.*` is imported
# anywhere, because app.config.get_settings() is cached on first use and
# app.database creates its engine at import time.
# ---------------------------------------------------------------------------
_TMP_DB_FD, _TMP_DB_PATH = tempfile.mkstemp(suffix=".db", prefix="ai_powered_crm_test_")
os.close(_TMP_DB_FD)
os.environ["DATABASE_URL"] = f"sqlite:///{_TMP_DB_PATH}"
os.environ["OPENAI_API_KEY"] = ""
os.environ["APP_ENV"] = "test"
os.environ["APP_RELOAD"] = "false"

from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _cleanup_test_db():
    yield
    engine.dispose()
    Path(_TMP_DB_PATH).unlink(missing_ok=True)


@pytest.fixture(autouse=True)
def _reset_database():
    """Give every test a clean set of tables."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client
