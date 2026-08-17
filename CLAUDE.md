# CLAUDE.md

Instructions for Claude Code when working in this repository.

## Project summary

`ai-powered-crm` is a FastAPI + SQLAlchemy + Jinja2 CRM application with AI features
powered by the OpenAI Responses API. SQLite is used by default; PostgreSQL is
supported by changing `DATABASE_URL`. There is no frontend build step - HTML
is server-rendered with Jinja2, and interactivity is handled by small vanilla
JS files in `app/static/js/`.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dev server (auto-reloading)
uvicorn app.main:app --reload

# Run tests
pytest -v

# Seed sample data
python -m scripts.seed_data

# Check for syntax errors quickly
python -m py_compile app/**/*.py
```

## Code conventions

- **Models** (`app/models/`): SQLAlchemy 2.0 declarative style with
  `Mapped[...]` type annotations. Every model inherits `IDMixin` and
  `TimestampMixin` from `app/models/base.py`.
- **Schemas** (`app/schemas/`): Pydantic v2. Each entity has `*Base`,
  `*Create`, `*Update` (all fields optional), and `*Read` (extends
  `TimestampedRead`).
- **Routers** (`app/routers/`): one file per entity, containing both HTML
  page routes (`router = APIRouter()`) and a JSON API
  (`api_router = APIRouter(prefix="/api/...")`). Both are registered in
  `app/main.py`.
- **Form handling**: HTML `POST` routes read form data with
  `await request.form()` and convert it to a dict with a local
  `_<entity>_form_to_dict()` helper before passing it to
  `app/services/crud.py`'s `create_obj` / `update_obj`.
- **AI features**: always go through `app/services/ai_service.py`. Never call
  the OpenAI SDK directly from a router - use `get_ai_service()` and catch
  `AIServiceError` so failures degrade gracefully instead of crashing.
- **Templates**: extend `app/templates/base.html`. Reusable pieces (notes
  panel, tasks panel, AI panels) live in `app/templates/partials/` and are
  included with Jinja `{% include %}`, relying on the default
  context-sharing behavior - set any variables the partial needs with
  `{% set %}` immediately before including it.
- **Styling**: use the existing CSS custom properties in
  `app/static/css/style.css` (`--accent`, `--surface`, `--border`, etc.)
  rather than hardcoding colors, so dark mode keeps working automatically.

## Testing conventions

- Tests live in `tests/`, one file per feature area.
- `tests/conftest.py` isolates every test run with a temporary SQLite
  database and disables AI (no API key), so tests are deterministic and
  never touch the developer's real data.
- When adding a new entity or endpoint, add a corresponding test file
  covering create/list/get/update/delete at minimum.
- Run `pytest -v` before considering any change complete.

## Things to avoid

- Don't add a frontend build step (no npm, no bundler) - this project is
  intentionally build-free.
- Don't call the OpenAI SDK outside of `app/services/ai_service.py`.
- Don't hardcode colors in templates or CSS - use the existing custom
  properties.
- Don't remove the AI graceful-fallback behavior (catching `AIServiceError`)
  - the app must always run without an API key configured.
