# ai-powered-crm - Complete Beginner's Setup & User Guide

Welcome! This guide assumes you have **never** used Python, Git, VS Code, a terminal, or a
virtual environment before. Follow every step in order and you'll have this AI-powered CRM
running on your own computer.

> **What is this app?** `ai-powered-crm` is a Customer Relationship Management tool - a place to
> track companies, contacts, leads, deals, tasks, and meetings, with AI helpers (email
> drafting, summaries, follow-up suggestions) powered by OpenAI. It runs entirely on your
> own computer; nothing is uploaded anywhere except optional calls to OpenAI's API.

---

## Table of Contents

1. [Install Python](#1-install-python)
2. [Install Git](#2-install-git-optional-but-recommended)
3. [Install Visual Studio Code](#3-install-visual-studio-code)
4. [Recommended VS Code Extensions](#4-recommended-vs-code-extensions)
5. [Open the Project](#5-open-the-project-in-vs-code)
6. [Create a Virtual Environment](#6-create-a-virtual-environment)
7. [Activate the Virtual Environment](#7-activate-the-virtual-environment)
8. [Install Dependencies](#8-install-dependencies)
9. [Create the .env File](#9-create-the-env-file)
10. [Configure the OpenAI API Key](#10-configure-the-openai-api-key-optional)
11. [Run the Application](#11-run-the-application)
12. [Test the Application](#12-test-the-application)
13. [Using Every Feature](#13-using-every-feature)
14. [Troubleshooting](#14-troubleshooting)
15. [FAQ](#15-faq)
16. [Common Mistakes](#16-common-mistakes)
17. [Security Recommendations](#17-security-recommendations)
18. [Next Learning Steps](#18-next-learning-steps)

---

## 1. Install Python

The app is written in **Python**, so your computer needs Python 3.11 or newer installed.

### Windows
1. Go to https://www.python.org/downloads/.
2. Click the big **"Download Python 3.x.x"** button.
3. Run the downloaded installer.
4. **Very important:** on the first installer screen, tick the checkbox at the bottom that
   says **"Add python.exe to PATH"** before clicking **Install Now**.
5. When it finishes, open a new terminal (see [Common Mistakes](#16-common-mistakes) if you
   don't know how) and type:
   ```
   python --version
   ```
   You should see something like `Python 3.12.4`. If you see an error, restart your computer
   and try again.

### macOS
1. Go to https://www.python.org/downloads/ and download the macOS installer.
2. Open the downloaded `.pkg` file and follow the installer.
3. Open the **Terminal** app (press `Cmd + Space`, type "Terminal", press Enter).
4. Type:
   ```
   python3 --version
   ```
   You should see `Python 3.11` or newer.

---

## 2. Install Git (optional, but recommended)

Git lets you download and manage source code. It isn't strictly required to *run* this
project (you likely already have the project files), but it's useful if you ever want to
update the code or contribute changes.

- **Windows:** download and install from https://git-scm.com/download/win (accept all
  default options).
- **macOS:** open Terminal and type `git --version`. If it isn't installed, macOS will
  prompt you to install the "Command Line Developer Tools" - click **Install**.

---

## 3. Install Visual Studio Code

Visual Studio Code (VS Code) is a free code editor that makes working with this project
much easier.

1. Go to https://code.visualstudio.com/.
2. Download the version for your operating system.
3. Run the installer and accept the defaults.

---

## 4. Recommended VS Code Extensions

Open VS Code, click the **Extensions** icon in the left sidebar (it looks like four small
squares), search for and install:

- **Python** (by Microsoft) - Python language support, debugging, and IntelliSense.
- **Pylance** (by Microsoft) - usually installs automatically with the Python extension.
- **Jinja** - syntax highlighting for the `.html` templates in `app/templates/`.
- **SQLite Viewer** - lets you browse the `data/ai_powered_crm.db` database file visually
  (optional, handy for debugging).

---

## 5. Open the Project in VS Code

1. Open VS Code.
2. Click **File -> Open Folder...**
3. Select the `ai-powered-crm` folder (the one containing `app/`, `requirements.txt`, etc.).
4. Click **Open**. You should see the project's file tree on the left.
5. Open a terminal *inside* VS Code: **Terminal -> New Terminal** (or press Ctrl+`).
   All the commands below are typed into this terminal.

---

## 6. Create a Virtual Environment

A **virtual environment** is an isolated folder that holds this project's own copy of
Python packages, so it doesn't interfere with anything else on your computer. Think of it
as a clean, private toolbox just for this project.

In the VS Code terminal, make sure you're inside the `ai-powered-crm` folder, then run:

**Windows:**
```
python -m venv .venv
```

**macOS:**
```
python3 -m venv .venv
```

This creates a new folder called `.venv` inside the project. That's normal and expected -
it's already excluded from Git via `.gitignore`.

---

## 7. Activate the Virtual Environment

Activating "switches on" the virtual environment so that Python and `pip` commands use the
project's private toolbox instead of your system-wide Python.

**Windows (Command Prompt / PowerShell):**
```
.venv\Scripts\activate
```

**macOS / Linux (bash/zsh):**
```
source .venv/bin/activate
```

You'll know it worked because your terminal prompt will now start with `(.venv)`.

> You must activate the virtual environment **every time** you open a new terminal to work
> on this project. The `Start App` scripts described later do this for you automatically.

---

## 8. Install Dependencies

With the virtual environment activated, install all the Python packages this project
needs:

```
pip install -r requirements.txt
```

This downloads and installs FastAPI, SQLAlchemy, the OpenAI SDK, and everything else listed
in `requirements.txt`. It may take a minute or two. You'll see a lot of text scroll by -
that's normal.

---

## 9. Create the .env File

The `.env` file holds your personal configuration (like your OpenAI API key) and is never
shared or committed to Git.

1. In the project folder, find the file named `.env.example`.
2. Make a copy of it and rename the copy to exactly `.env` (no `.example` at the end).
   - **Windows (terminal):** `copy .env.example .env`
   - **macOS (terminal):** `cp .env.example .env`
   - Or just copy/paste and rename the file in VS Code's file explorer.
3. Open `.env` in VS Code. You'll see settings like `APP_PORT`, `DATABASE_URL`, and
   `OPENAI_API_KEY`. The defaults work out of the box - you only need to change
   `OPENAI_API_KEY` if you want AI features (see next section).

---

## 10. Configure the OpenAI API Key (optional)

The CRM works perfectly well **without** an OpenAI key - every core feature (companies,
contacts, leads, deals, tasks, notes, meetings, calendar, search, reports) works with zero
configuration. The **AI features** (lead summaries, email drafting, follow-up suggestions,
customer insights) additionally require an OpenAI API key.

1. Create an account at https://platform.openai.com/.
2. Go to https://platform.openai.com/api-keys and click **Create new secret key**.
3. Copy the key (it starts with `sk-`).
4. Open your `.env` file and replace:
   ```
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ```
   with your real key, e.g.:
   ```
   OPENAI_API_KEY=sk-abc123...
   ```
5. Save the file.

> **Note:** OpenAI API usage costs money based on how much you use it (usually fractions of
> a cent per request for this app's short prompts). Set a usage limit in your OpenAI
> dashboard if you're concerned about cost. Never share your key with anyone, and never
> commit `.env` to Git - `.gitignore` already prevents this by default.

---

## 11. Run the Application

You have two options:

### Option A - Double-click startup scripts (easiest)
- **Windows:** double-click `Start App.bat`.
- **macOS:** double-click `Start App (Mac).command` (see the Troubleshooting section if
  macOS blocks it the first time).

These scripts automatically create the virtual environment (if needed), install
dependencies, check your `.env` file, and launch the app.

### Option B - Manual command (with the virtual environment activated)
```
uvicorn app.main:app --reload
```

Once running, open your web browser and go to:

```
http://127.0.0.1:8000
```

You should see the ai-powered-crm dashboard. To stop the server, click back in the terminal window
and press `Ctrl + C`.

---

## 12. Test the Application

The project ships with an automated test suite (33 tests) covering every major feature.
With the virtual environment activated, run:

```
pytest -v
```

All tests should pass. Tests run against a temporary, isolated database, so running them
never touches your real data in `data/ai_powered_crm.db`.

You can also manually test the app by clicking through it in your browser:
- Visit `http://127.0.0.1:8000/health` - you should see a small JSON response confirming
  the app is running.
- Create a company, a contact, and a lead through the UI and confirm they appear in their
  respective lists.

---

## 13. Using Every Feature

Once the app is running at `http://127.0.0.1:8000`, use the top navigation bar to explore:

| Feature | What it does |
|---|---|
| **Dashboard** (`/`) | KPI overview, pipeline snapshot, upcoming meetings, recent leads. |
| **Companies** (`/companies`) | Add/edit/delete organizations you sell to. |
| **Contacts** (`/contacts`) | People associated with companies. |
| **Customers** (`/customers`) | Converted, paying accounts with lifetime value tracking. |
| **Leads** (`/leads`) | Inbound/outbound opportunities with scoring and status. Click the AI summary action on a lead's detail page to generate an AI summary (requires an API key). |
| **Pipeline** (`/pipeline`) | Drag-and-drop Kanban board of deals across sales stages. |
| **Tasks** (`/tasks`) | To-dos with priority and due dates, linkable to any record. |
| **Notes** (`/notes`) | Freeform notes attachable to any record. |
| **Meetings** (`/meetings`) | Schedule meetings with agendas and attendees; summarize notes with AI. |
| **Calendar** (`/calendar`) | Unified month view combining tasks and meetings. |
| **Search** (`/search`) | Global search across companies, contacts, customers, leads, and deals. |
| **Reports** (`/reports`) | Pipeline value, win rate, lead source breakdown, and more. |
| **Dark Mode** | Toggle in the navigation bar; your choice is remembered between visits. |

### AI features (require `OPENAI_API_KEY` in `.env`)
- **Lead summarization** - on a lead's page, use the AI summary action.
- **Email drafting** - available from contact/lead/customer detail pages.
- **Meeting summaries** - paste raw notes on a meeting page and generate a structured
  summary.
- **Follow-up suggestions** - get 3-5 actionable next steps for any record.
- **Customer insights** - health, churn/upsell risk analysis for customer accounts.

If no API key is configured, these panels show a friendly message instead of an error - the
rest of the app keeps working normally.

### Sample data
To populate the CRM with realistic sample data for exploring the UI, run (with the virtual
environment activated):
```
python -m scripts.seed_data
```

---

## 14. Troubleshooting

**"python is not recognized as an internal or external command" (Windows)**
Python wasn't added to PATH during installation. Reinstall Python and make sure to tick
"Add python.exe to PATH", or search "Environment Variables" in the Windows Start menu and
add your Python install folder manually.

**"command not found: python" (macOS)**
Use `python3` instead of `python` - macOS often only registers the `python3` command.

**macOS says the app "cannot be opened because it is from an unidentified developer"**
Right-click (or Control-click) `Start App (Mac).command`, choose **Open**, then click
**Open** again in the confirmation dialog. You only need to do this once.

**The browser shows "This site can't be reached" at 127.0.0.1:8000**
The server probably isn't running, or it crashed. Check the terminal window for red error
text. Make sure no other application is already using port 8000 (change `APP_PORT` in
`.env` if needed).

**"ModuleNotFoundError: No module named 'fastapi'" (or similar)**
Your virtual environment isn't activated, or dependencies weren't installed. Run the
activation command from step 7, then `pip install -r requirements.txt` again.

**AI features show "AI features are not configured"**
You haven't set a valid `OPENAI_API_KEY` in `.env`, or it still contains the placeholder
value `sk-your-openai-api-key-here`. See step 10.

**Port 8000 is already in use**
Another program (possibly another copy of this app) is using that port. Either stop that
program, or change `APP_PORT` in `.env` to something else (e.g. `8001`) and restart.

**I deleted or corrupted my database and want a fresh start**
Stop the app, delete `data/ai_powered_crm.db`, and restart - a new empty database is created
automatically.

---

## 15. FAQ

**Do I need to know how to code to use this app?**
No - once it's running, it's a normal point-and-click web application. Coding knowledge is
only needed if you want to customize it.

**Is my data sent to the internet?**
Only when you explicitly use an AI feature (email drafting, summaries, etc.), in which case
the relevant record's text is sent to OpenAI's API. Everything else stays entirely on your
computer in the local SQLite database file (`data/ai_powered_crm.db`).

**Can I use this with a real team / in production?**
The app is designed as a learning/personal project and local development tool. See the
Security Recommendations section and `PROJECT_REVIEW.md` before considering any kind of
shared or public deployment - as shipped, it has no user login or access control.

**Can I switch from SQLite to PostgreSQL?**
Yes - change `DATABASE_URL` in `.env` to a PostgreSQL connection string (an example is
commented out in `.env.example`). No application code changes are required.

**How do I stop the app?**
Click into the terminal window running the server and press `Ctrl + C`.

---

## 16. Common Mistakes

- **Forgetting to activate the virtual environment** before running `pip install` or
  `uvicorn` - you'll get "module not found" errors.
- **Editing `.env.example` instead of `.env`** - your changes won't take effect. Always
  edit the copy named exactly `.env`.
- **Committing `.env` to Git** - it's excluded by `.gitignore` by default; don't remove
  that line.
- **Opening the wrong folder in VS Code** - make sure you open the `ai-powered-crm` folder itself,
  not its parent folder.
- **Using `python` instead of `python3` on macOS**, or vice versa on Windows.
- **Not restarting the terminal** after a fresh Python install on Windows.

---

## 17. Security Recommendations

- Never commit your real `.env` file or API keys to Git or share them publicly.
- Rotate your OpenAI API key immediately if you ever accidentally expose it.
- This app has **no built-in authentication** - anyone with network access to the port it
  runs on can view and edit all data. Only run it on `127.0.0.1` (the default) unless you
  add proper authentication first.
- Change `SECRET_KEY` in `.env` before any deployment beyond your own machine, even though
  it isn't currently wired into any session mechanism (see `PROJECT_REVIEW.md`).
- If you add PostgreSQL, use a dedicated database user with a strong, unique password -
  never reuse passwords across services.

---

## 18. Next Learning Steps

Once you're comfortable running the app, here are good next steps:

1. Read `docs/ARCHITECTURE.md` to understand how the FastAPI app is structured.
2. Read `docs/API.md` for the full JSON API reference.
3. Explore `app/routers/` - each file is a self-contained example of FastAPI routing,
   SQLAlchemy queries, and Jinja2 templates.
4. Try adding a new field to an existing entity (e.g., a "priority" field on Companies) and
   trace it through the model, schema, router, and template.
5. Learn the basics of Git (`git init`, `git add`, `git commit`) so you can track your own
   changes.
6. Read up on FastAPI's official tutorial at https://fastapi.tiangolo.com/tutorial/ to
   deepen your understanding of the framework powering this app.

You're all set - enjoy exploring ai-powered-crm!
