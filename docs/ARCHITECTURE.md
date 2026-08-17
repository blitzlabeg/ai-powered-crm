# Architecture

This document explains how `ai-powered-crm` is put together: the layers, the data
model, and the reasoning behind key design decisions.

## 1. High-level overview

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                          Browser (User)                          â”‚
â”‚      HTML pages (Jinja2) + small vanilla JS (dark mode, AI,      â”‚
â”‚                     Kanban drag-and-drop)                        â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                 â”‚ HTTP
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                         FastAPI application                       â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚  â”‚  Routers       â”‚   â”‚  Schemas        â”‚   â”‚  Services           â”‚ â”‚
â”‚  â”‚  (HTML pages   â”‚â”€â”€â–¶â”‚  (Pydantic      â”‚   â”‚  - AI service        â”‚ â”‚
â”‚  â”‚   + JSON API)  â”‚   â”‚   validation)   â”‚   â”‚    (OpenAI Responses)â”‚ â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚  - CRUD helpers       â”‚ â”‚
â”‚          â”‚                                  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚          â–¼                                             â”‚             â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚  â”‚                    SQLAlchemy ORM Models                        â”‚ â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                    â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚   SQLite (dev) / PostgreSQL     â”‚
                    â”‚           (prod)                â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

## 2. Why server-rendered HTML instead of a JS framework?

- **Zero build step.** No `npm install`, no bundler, no `node_modules`. A
  beginner can run this project with nothing but Python installed.
- **FastAPI + Jinja2 is a proven, boring, reliable combination** for CRUD-heavy
  internal tools like a CRM.
- **Progressive enhancement.** Every page works with plain HTML forms; small
  vanilla JS files layer on interactivity (AI panels via `fetch()`, Kanban
  drag-and-drop, dark mode) without requiring a SPA framework.

## 3. Request flow

Each feature (Companies, Contacts, Leads, etc.) has **one router file** under
`app/routers/` that defines both:

1. **HTML page routes** (`GET /companies`, `GET /companies/{id}`, `POST
   /companies/new`, â€¦) that render Jinja2 templates and handle HTML form
   submissions.
2. **A JSON API router** (`/api/companies/...`) with full CRUD, validated by
   Pydantic schemas in `app/schemas/`.

Both sets of routes share the same SQLAlchemy models and the same generic CRUD
helpers in `app/services/crud.py` (`get_or_404`, `create_obj`, `update_obj`,
`delete_obj`), so there is a single source of truth for how records are
persisted.

## 4. Data model

```
Company 1â”€â”€â”€* Contact 1â”€â”€â”€1 Customer
   â”‚              â”‚              â”‚
   â”‚              â””â”€â”€â”€* Lead     â”‚
   â”‚                             â”‚
   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€* Deal â”€â”€â”€â”€â”€â”€â”€â”˜
                     â”‚
   Task / Note / Meeting â”€â”€(generic related_type + related_id)â”€â”€â–¶ any entity
```

- **Company** â€” an organization.
- **Contact** â€” a person, optionally linked to a `Company`.
- **Customer** â€” a converted account; optionally linked to a `Contact` and/or
  `Company`. Tracks `status` and `lifetime_value`.
- **Lead** â€” a sales opportunity not yet converted; has `status`, `source`,
  `score`, and an `ai_summary` field populated by the AI summarization feature.
- **Deal** â€” an opportunity actively moving through the sales pipeline
  (`stage`, `value`, `probability`); has an `ai_recommendation` field.
- **Task** â€” a to-do item. Uses a **generic polymorphic relationship**
  (`related_type` + `related_id`) so a task can point at *any* other entity
  without needing a foreign key column per entity type.
- **Note** â€” freeform text, same generic relationship pattern as `Task`.
- **Meeting** â€” scheduled event with an `ai_summary` field.

### Why the generic `related_type` / `related_id` pattern for Task and Note?

Adding a dedicated foreign key column to `Task` and `Note` for every entity
type (`company_id`, `contact_id`, `lead_id`, `deal_id`, â€¦) would work, but it
means every new entity type requires a schema migration on `Task` and `Note`.
The generic pattern trades a small amount of type safety (no database-level
foreign key constraint) for flexibility â€” new entity types don't require
touching `Task` or `Note` at all. This is a common, pragmatic CRM pattern.

## 5. AI integration

All AI calls go through `app/services/ai_service.py`, a thin wrapper around
the **OpenAI Responses API** (`client.responses.create(...)`). Design goals:

- **Single system prompt** (`SYSTEM_PROMPT`) shared across all AI features,
  so tone and behavior stay consistent.
- **Graceful degradation.** If `OPENAI_API_KEY` is not configured, or the API
  call fails for any reason, `AIServiceError` is raised and every calling
  router catches it and stores/returns a friendly, non-crashing message. The
  rest of the app keeps working normally.
- **No secrets in the browser.** The API key never leaves the server; the
  frontend calls `/api/ai/...` endpoints, which call OpenAI server-side.

## 6. Configuration

`app/config.py` uses `pydantic-settings` to load configuration from
environment variables and an optional `.env` file. `get_settings()` is
cached with `lru_cache` so settings are parsed once per process.

## 7. Database portability

`app/database.py` builds the SQLAlchemy engine from a single `DATABASE_URL`.
SQLite gets a `check_same_thread: False` connect arg (required for use with
FastAPI's threaded request handling); PostgreSQL does not need this. No other
code differs between the two â€” this is the benefit of using SQLAlchemy's ORM
layer rather than raw, database-specific SQL.

## 8. Testing strategy

`tests/conftest.py` points `DATABASE_URL` at a fresh temporary SQLite file
*before* the application is imported, and recreates all tables before every
test function. This means:

- Tests never touch your real `data/ai_powered_crm.db`.
- Tests are fully isolated from each other.
- No API key is configured during tests, which also exercises and verifies
  the AI graceful-fallback behavior described above.

## 9. Front-end structure

- `app/static/css/style.css` â€” a single stylesheet using CSS custom
  properties for theming (light/dark mode switches by swapping variable
  values on `<html data-theme="...">`).
- `app/static/js/app.js` â€” dark mode toggle, mobile sidebar toggle, delete
  confirmations, and Kanban drag-and-drop.
- `app/static/js/ai.js` â€” `fetch()`-based handlers for the AI panels that
  render results inline without a full page reload.
