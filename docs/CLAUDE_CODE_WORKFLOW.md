# Building and Maintaining ai-powered-crm with Claude Code

This document demonstrates the workflows Claude Code is good at, using
`ai-powered-crm` itself as the running example. It's meant both as a record of how
this project was built and as a template for how *you* can keep extending it
using Claude Code from the VS Code integrated terminal.

Every example below is a real prompt you can type into Claude Code inside
this repository.

---

## 1. Project generation

Claude Code is effective at scaffolding a new feature end-to-end â€” model,
schema, router, templates, and tests â€” in one pass, because it can read the
existing patterns in the repo and match them.

**Example prompt:**
```
Add a new "Products" entity to ai-powered-crm, following the same pattern as
Company: a SQLAlchemy model in app/models/product.py, Pydantic schemas in
app/schemas/product.py, a router in app/routers/products.py with both HTML
pages and a JSON API, Jinja2 templates under app/templates/products/, and
register everything in app/main.py. Add it to the sidebar nav in
app/templates/base.html. Write tests in tests/test_products.py.
```

Claude Code will:
1. Read `app/models/company.py` and `app/routers/companies.py` as reference.
2. Generate the new files following the exact same conventions (type hints,
   docstrings, the `_form_to_dict` helper pattern, etc.).
3. Wire up imports in `app/main.py`.
4. Run `pytest` to confirm the new tests pass.

---

## 2. Refactoring

Claude Code shines at **mechanical, repository-wide refactors** that would be
tedious and error-prone by hand.

**Example prompt:**
```
The _form_to_dict() helper functions in app/routers/*.py are nearly
identical. Extract a shared helper into app/services/forms.py that takes a
field spec and returns a clean dict, then update every router to use it.
Keep all existing behavior identical â€” run the test suite after each file
you change.
```

**Example prompt (renaming across the codebase):**
```
Rename the Deal model's `probability` field to `win_probability` everywhere:
the model, schemas, routers, templates, JS, and tests. Show me a diff
summary when you're done.
```

Claude Code will use its file-editing tools to make consistent changes across
every affected file, then re-run `pytest` to make sure nothing broke.

---

## 3. Debugging

**Example prompt:**
```
When I POST to /pipeline/{id}/stage with an invalid stage value, I'm getting
a 500 error instead of a clean 400. Find out why and fix it, then add a
regression test.
```

Claude Code will:
1. Search `app/routers/pipeline.py` for the `/stage` endpoint.
2. Reproduce the bug by reading the code path (`DealStage(new_stage)` raising
   an uncaught `ValueError`).
3. Fix it (this exact bug is already fixed in `app/routers/pipeline.py` â€”
   see the `try/except ValueError` block in `move_deal_stage`).
4. Add `tests/test_pipeline.py::test_move_deal_stage_rejects_invalid_stage`
   as a regression test.

**Example prompt (using the terminal):**
```
Run the app locally in the background, then use curl to reproduce a bug
where creating a Lead without a title crashes. Show me the traceback and
propose a fix.
```

Claude Code can run `uvicorn app.main:app &`, use `curl` to hit the endpoint,
read the traceback from the terminal output, and patch the code.

---

## 4. Testing

**Example prompt:**
```
Look at tests/test_companies.py and write an equivalent, equally thorough
test file for the Meetings API in tests/test_meetings_extra.py, covering
create, list, get, update, delete, and the /summarize AI-fallback endpoint.
```

**Example prompt (coverage):**
```
Install pytest-cov, run the test suite with coverage, and tell me which
files in app/routers/ have the lowest test coverage. Then write tests to
bring the lowest one above 80%.
```

```bash
pip install pytest-cov
pytest --cov=app --cov-report=term-missing
```

---

## 5. Documentation

**Example prompt:**
```
I just added the Products entity from the example above. Update
README.md's feature list, docs/API.md's endpoint table, and
docs/ARCHITECTURE.md's data model diagram to include it.
```

Claude Code is well-suited to keeping documentation in sync with code changes
because it can read both simultaneously and cross-reference them â€” for
example, verifying every route in `app/routers/` has a corresponding entry in
`docs/API.md`.

---

## 6. Terminal workflow

A typical Claude Code session for this project, run from the integrated
terminal in VS Code:

```bash
# Start a Claude Code session in the project root
cd ai-powered-crm
claude

# Inside the session, you can ask Claude Code to:
#  - run the test suite
#  - start the dev server
#  - inspect git history
#  - install a new dependency
#  - run database migrations
# ...and it will use the terminal directly rather than just suggesting commands.
```

Common terminal commands Claude Code will use on your behalf during a
session (shown here for reference â€” you don't need to type these yourself,
just ask in plain English):

```bash
# Run the test suite
pytest -v

# Run a single test file
pytest tests/test_leads.py -v

# Start the dev server with auto-reload
uvicorn app.main:app --reload

# Check for syntax errors across the whole app without running it
python -m py_compile app/**/*.py

# Format code
pip install black && black app tests

# Lint
pip install ruff && ruff check app tests

# Inspect recent changes before committing
git status
git diff

# Create a commit
git add -A
git commit -m "Add Products entity following the Company pattern"
```

---

## 7. Suggested next steps to practice with Claude Code

Try these prompts yourself, in order of increasing difficulty:

1. *"Add a `favorite` boolean column to the Contact model, a migration for
   it, and a star icon toggle on the contact list page."*
2. *"Add pagination to the Companies list page â€” 25 per page, with Prev/Next
   links that preserve the search query."*
3. *"Add a simple username/password login using FastAPI's session
   middleware, and protect every route except /health behind it."*
4. *"Write an Alembic migration setup (alembic init, env.py wired to our
   Base.metadata) so future schema changes don't require dropping the
   database."*
5. *"Add a CSV export button to the Reports page that downloads the current
   pipeline as a CSV file."*

Each of these is a realistic, scoped task that exercises project generation,
refactoring, debugging, testing, and documentation â€” the same skills
demonstrated throughout this file.
