# ai-powered-crm

An AI-powered Customer Relationship Management (CRM) application built with **FastAPI**,
**SQLAlchemy**, **SQLite/PostgreSQL**, and the **OpenAI Responses API**.

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![Claude](https://img.shields.io/badge/Claude-Code-A33AFFFF?style=for-the-badge&logo=claude)

---

## Features

### Core CRM
- **Dashboard** - KPIs, pipeline snapshot, upcoming meetings, recent leads
- **Companies** - organizations you sell to
- **Contacts** - people at those companies
- **Customers** - converted, paying accounts with lifetime value tracking
- **Leads** - inbound/outbound opportunities with scoring and source tracking
- **Sales Pipeline** - drag-and-drop Kanban board across deal stages
- **Tasks** - to-dos with priority, due dates, and links to any record
- **Notes** - freeform notes attachable to any record
- **Meetings** - scheduling with agendas, attendees, and notes
- **Calendar** - unified month view of tasks and meetings
- **Search** - global search across companies, contacts, customers, leads, and deals
- **Reports** - pipeline value, win rate, lead sources, task/customer breakdowns
- **Dark Mode** - persisted, system-independent theme toggle

### AI Features (OpenAI Responses API)
- **Lead summarization** - turn a lead record into a crisp executive summary
- **Email drafting** - generate ready-to-send emails from a purpose and context
- **Meeting summaries** - convert raw notes into overview / decisions / action items
- **Follow-up suggestions** - actionable next steps for any record
- **Customer insights** - health, churn/upsell risk, and recommended actions
- **Sales recommendations** - AI coaching on how to move a deal forward

All AI features **degrade gracefully**: if no `OPENAI_API_KEY` is configured, the app
still runs perfectly - AI panels show a friendly notice instead of crashing.

---

## Technology Stack

| Layer         | Technology                                   |
|---------------|-----------------------------------------------|
| Backend       | Python 3.11+, FastAPI                         |
| ORM           | SQLAlchemy 2.0 (typed models)                 |
| Database      | SQLite (default) or PostgreSQL                |
| Templates     | Jinja2 (server-rendered HTML)                 |
| Frontend      | Vanilla HTML / CSS / JavaScript (no build step) |
| AI            | OpenAI Responses API                          |
| Testing       | Pytest + FastAPI TestClient                   |

No Node.js, no bundler, no frontend framework - the UI is server-rendered HTML with
small, focused vanilla JS files for interactivity (dark mode, Kanban drag-and-drop, AI
panels). This keeps the project approachable and fast to run.

---

## Quick Start

### Prerequisites

- Python 3.11+
- (Optional) An OpenAI API key to enable AI features

### 1. Clone and set up

```bash
# Clone or download this repository, then enter it
cd ai-powered-crm

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
# Copy the example env file and edit it
cp .env.example .env
# then open .env and add your OPENAI_API_KEY (optional for AI features)
```

### 3. Run the app

```bash
uvicorn app.main:app --reload
```

Open your browser at http://127.0.0.1:8000.

### 4. (Optional) Load sample data

```bash
python -m scripts.seed_data
```

This populates the database with sample companies, contacts, leads, deals,
tasks, and meetings so the UI is not empty on first run.

### Running tests

```bash
pytest -v
```

The test suite uses an isolated temporary SQLite database per run, so it never
touches your real data. AI features are tested without an API key configured.

---

## Switching to PostgreSQL

By default, `ai-powered-crm` uses SQLite (`sqlite:///./data/ai_powered_crm.db`) -
zero setup required. To use PostgreSQL instead, change one line in `.env`:

```
DATABASE_URL=postgresql+psycopg2://crm_user:crm_password@localhost:5432/ai_crm
```

No application code changes are needed - SQLAlchemy and the connection logic in
`app/database.py` handle both transparently.

---

## Project Structure

```
ai-powered-crm/
  app/
    main.py             # FastAPI app entrypoint
    config.py           # Settings (pydantic-settings)
    database.py         # SQLAlchemy engine/session setup
    templating.py       # Jinja2 environment + custom filters
    models/             # SQLAlchemy ORM models
    schemas/            # Pydantic request/response schemas
    routers/            # FastAPI routers (HTML pages + JSON API)
    services/           # AI service, generic CRUD helpers
    templates/          # Jinja2 HTML templates
    static/             # CSS and JavaScript (no build step)
  scripts/
    seed_data.py        # Sample data generator
  tests/                # Pytest test suite
  docs/                 # Architecture & API documentation
  requirements.txt
  pyproject.toml
  .env.example
  README.md
  LICENSE
```

See [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) for a deeper explanation of how
the pieces fit together, and [`docs/API.md`](./docs/API.md) for the JSON API reference.

---

## Environment Variables

See [`.env.example`](./.env.example) for the full list. The important ones:

| Variable           | Description                       | Default                          |
|--------------------|-----------------------------------|----------------------------------|
| `DATABASE_URL`     | SQLAlchemy connection string      | `sqlite:///./data/ai_powered_crm.db` |
| `OPENAI_API_KEY`   | Your OpenAI API key (enables AI)  | *(empty)*                        |
| `OPENAI_MODEL`     | Model used for the OpenAI API     | `gpt-4o-mini`                    |
| `APP_HOST` / `APP_PORT` | Where the server listens    | `127.0.0.1:8000`                 |

---

## License

MIT - use this project as a learning reference, a starter template, or a base for your own CRM.
See [LICENSE](./LICENSE) for details.

### Contributors

- **Blitz** - initial development and maintenance.
- **Claude (Anthropic)** - code generation, documentation, and testing assistance.

---

## Acknowledgements

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [OpenAI](https://openai.com/)
- [Claude Code](https://claude.com/claude-code) for development assistance
