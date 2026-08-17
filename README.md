# ai-powered-crm

An AI-powered Customer Relationship Management (CRM) application built with **FastAPI**,
**SQLAlchemy**, **SQLite/PostgreSQL**, and the **OpenAI Responses API**.

This project was designed and built to be developed with **[Claude Code](https://claude.com/claude-code)**
as the primary development tool - the codebase, structure, and docs reflect the kind of
production-quality output you get when using Claude Code from the terminal inside VS Code.

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![Claude](https://img.shields.io/badge/Claude-Code-A33AFFFF?style=for-the-badge&logo=claude)

---

## âœ¨ Features

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
- **Email drafting** - generate ready-to-send emails from a purpose + context
- **Meeting summaries** - convert raw notes into overview / decisions / action items
- **Follow-up suggestions** - actionable next steps for any record
- **Customer insights** - health, churn/upsell risk, and recommended actions
- **Sales recommendations** - AI coaching on how to move a deal forward

All AI features **degrade gracefully**: if no `OPENAI_API_KEY` is configured, the app
still runs perfectly - AI panels show a friendly notice instead of crashing.

---

## ðŸ›  Technology Stack

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

## ðŸš€ Quick Start

### The easy way (recommended for beginners)

- **Windows:** double-click `Start App.bat`
- **macOS:** double-click `Start App (Mac).command`

Both scripts will check for Python, create a virtual environment, install
dependencies, verify your `.env` file, and launch the app automatically at
`http://127.0.0.1:8000`.

ðŸ‘‰ **New to Python, VS Code, Git, or Claude Code?** Read [`INSTRUCTION.md`](./INSTRUCTION.md)
for a complete, zero-assumptions walkthrough.

### The manual way

```bash
# 1. Clone or download this repository, then enter it
cd ai-powered-crm

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# then edit .env and add your OPENAI_API_KEY

# 5. Run the app
uvicorn app.main:app --reload

# 6. Open your browser
# http://127.0.0.1:8000
```

### Load sample data (optional but recommended)

```bash
python -m scripts.seed_data
```

This populates the database with sample companies, contacts, leads, deals,
tasks, and meetings so the UI isn't empty on first run.

---

## ðŸ§ª Running Tests

```bash
pytest
```

The test suite spins up an isolated temporary SQLite database per run, so it
never touches your real `data/ai_powered_crm.db` file. AI features are tested with no
API key configured to verify the graceful-fallback behavior.

---

## ðŸ—„ Switching to PostgreSQL

By default, `ai-powered-crm` uses SQLite (`sqlite:///./data/ai_powered_crm.db`) - zero setup
required. To use PostgreSQL instead, just change one line in `.env`:

```env
DATABASE_URL=postgresql+psycopg2://crm_user:crm_password@localhost:5432/ai_powered_crm
```

No application code changes are needed - SQLAlchemy and the connection logic
in `app/database.py` handle both transparently.

---

## ðŸ“ Project Structure

```
ai-powered-crm/
â”œâ”€â”€ app/
â”‚   â”œâ”€â”€ main.py # FastAPI app entrypoint
â”‚   â”œâ”€â”€ config.py # Settings (pydantic-settings)
â”‚   â”œâ”€â”€ database.py # SQLAlchemy engine/session setup
â”‚   â”œâ”€â”€ templating.py # Jinja2 environment + custom filters
â”‚   â”œâ”€â”€ models/ # SQLAlchemy ORM models
â”‚   â”œâ”€â”€ schemas/ # Pydantic request/response schemas
â”‚   â”œâ”€â”€ routers/ # FastAPI routers (HTML pages + JSON API)
â”‚   â”œâ”€â”€ services/ # AI service, generic CRUD helpers
â”‚   â”œâ”€â”€ templates/ # Jinja2 HTML templates
â”‚   â””â”€â”€ static/ # CSS and JavaScript (no build step)
â”œâ”€â”€ scripts/
â”‚   â””â”€â”€ seed_data.py # Sample data generator
â”œâ”€â”€ tests/ # Pytest test suite
â”œâ”€â”€ docs/ # Architecture & workflow documentation
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ pyproject.toml
â”œâ”€â”€ .env.example
â”œâ”€â”€ Start App.bat # Windows one-click launcher
â”œâ”€â”€ Start App (Mac).command # macOS one-click launcher
â”œâ”€â”€ README.md
â””â”€â”€ INSTRUCTION.md # Beginner's guide to running this project
```

See [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) for a deeper explanation
of how the pieces fit together.

---

## ðŸ“š Documentation

| Document | Purpose |
|---|---|
| [`INSTRUCTION.md`](./INSTRUCTION.md) | Complete beginner's guide - install Python, VS Code, Git, Claude Code, and run this project from zero |
| [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) | System architecture, data model, and design decisions |
| [`docs/API.md`](./docs/API.md) | JSON API reference for every endpoint |
| [`docs/CLAUDE_CODE_WORKFLOW.md`](./docs/CLAUDE_CODE_WORKFLOW.md) | How this project was built and maintained with Claude Code (generation, refactoring, debugging, testing, docs) |
| [`CLAUDE.md`](./CLAUDE.md) | Project-specific instructions for Claude Code |

---

## ðŸ”’ Environment Variables

See [`.env.example`](./.env.example) for the full list. The important ones:

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | SQLAlchemy connection string | `sqlite:///./data/ai_powered_crm.db` |
| `OPENAI_API_KEY` | Your OpenAI API key (enables AI features) | *(empty)* |
| `OPENAI_MODEL` | Model used for the Responses API | `gpt-4o-mini` |
| `APP_HOST` / `APP_PORT` | Where the server listens | `127.0.0.1:8000` |

---

## ðŸ“„ License

MIT - use this project as a learning reference, a starter template, or a base
for your own CRM.
