# cursor-quality-tricks

A **tutorial repo** for running automated code quality checks and tests so that Cursor (or any developer) can validate changes before committing. The app is a simple Book Library API; the focus is on the **quality pipeline** around it.

## Book Library API – FastAPI CRUD Tutorial

A simple **Book Library** application demonstrating full CRUD operations with FastAPI, SQLite, and a minimal web UI.

### Domain: Book Library

- **Books** have: title, author, genre, year published, and availability status
- Perfect for learning: Create, Read, Update, Delete patterns

### Quick Start

```bash
pip install -r library-api/requirements.txt
python run.py
```

Open **http://127.0.0.1:8100** for the web UI, or **http://127.0.0.1:8100/docs** for the interactive API docs.

If port 8100 is already in use, stop the existing process first (e.g. `pkill -f "uvicorn main:app"` or close the terminal running it).

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/books` | List all books |
| GET | `/api/books/{id}` | Get one book |
| POST | `/api/books` | Create a book |
| PUT | `/api/books/{id}` | Update a book |
| DELETE | `/api/books/{id}` | Delete a book |

### Project Structure

```
library-api/
├── main.py       # FastAPI app, routes, static serving
├── models.py     # Pydantic schemas (request/response)
├── schemas.py    # SQLAlchemy ORM model
├── database.py   # SQLite connection
├── crud.py       # Database operations
├── static/       # Web UI
│   ├── index.html
│   ├── style.css
│   └── app.js
└── requirements.txt
```

Sample books are seeded on first run.

### Code Quality and Testing

This repo is set up so that **Cursor (and you) can run automated checks before committing**. Run everything from the repo root via the Makefile.

**First-time setup (dev dependencies):**

```bash
pip install -r library-api/requirements-dev.txt
```

**Run the full quality pipeline (lint, format, typecheck, complexity, tests):**

```bash
make check
```

Or run individual steps:

| Command | Description |
|---------|-------------|
| `make test` | Run pytest |
| `make lint` | Ruff lint |
| `make format` | Ruff format |
| `make quality` | Radon cyclomatic complexity + maintainability |
| `make typecheck` | mypy |

**Before committing or pushing:** Always run `make check` and fix any failures. See [AGENTS.md](AGENTS.md) for Cursor-oriented instructions.

### Testing

Tests live in `library-api/tests/`:

- `test_crud.py` – CRUD operations against the DB
- `test_api.py` – HTTP API endpoints
- `test_models.py` – Pydantic validation

Run tests: `make test` or `pytest` from the repo root.

---

## Tutorial: What We Built and How the Pipeline Works

This section explains what was set up, how the pipeline runs, and how to use it as a tutorial for “quality before commit.”

### What we’ve done

We added a **single-command quality gate** so that nothing gets committed without passing:

1. **Linting** – Ruff checks style and common bugs.
2. **Formatting** – Ruff enforces consistent code style.
3. **Type checking** – mypy checks types in the Python code.
4. **Complexity / maintainability** – Radon reports cyclomatic complexity and maintainability index.
5. **Automated tests** – Pytest runs unit and API tests against an in-memory database.

All of this is triggered from the repo root with:

```bash
make check
```

If anything fails, the command exits with an error so you (or Cursor) fix issues before committing.

### How the pipeline works

The pipeline is driven by a **Makefile** at the repo root. Each step is a separate target; `make check` runs them in sequence:

```
make check
    → make lint      (Ruff: style and lint rules)
    → make format    (Ruff: format code)
    → make typecheck (mypy: static types)
    → make quality   (Radon: complexity + maintainability)
    → make test      (pytest: all tests)
```

- **Order**: Lint and format run first so style is consistent; then typecheck and quality; then tests. If one step fails, the rest still run (you see all failures at once).
- **Single entry point**: Use `make check` (or `make all`) before every commit. Cursor is instructed to do this via [AGENTS.md](AGENTS.md).
- **Individual steps**: You can run `make test`, `make lint`, `make format`, `make quality`, or `make typecheck` alone when working on a specific kind of fix.

### Types of automated checks and tests

| Layer | Tool | What it does |
|-------|------|----------------|
| **Lint** | Ruff | Catches unused imports, style issues, simple bugs; enforces import order. Config in `pyproject.toml`. |
| **Format** | Ruff | Formats Python code (line length, quotes, etc.) so the codebase stays consistent. |
| **Types** | mypy | Checks type hints; finds type mismatches and missing annotations. We use `ignore_missing_imports` for third-party libs. |
| **Complexity** | Radon | **Cyclomatic complexity** (per function/class) and **maintainability index** (per file). Helps keep functions small and maintainable. |
| **Unit / integration** | pytest | **CRUD tests** (`test_crud.py`): create, read, update, delete against an in-memory SQLite DB. **API tests** (`test_api.py`): HTTP GET/POST/PUT/DELETE via FastAPI `TestClient`. **Model tests** (`test_models.py`): Pydantic validation (required fields, bounds, invalid input). |

Tests use **in-memory SQLite** and a **dependency override** for `get_db`, so the app code is not changed and the real database is never touched.

### Using this as a tutorial

1. **Run the gate**: From the repo root, run `make check`. Everything should pass. Use this as the “green baseline.”
2. **Break something on purpose**: Change a type, remove a test assertion, or add a too-complex function. Run `make check` again and fix what fails (lint, typecheck, quality, or tests).
3. **Add a feature**: Add a new endpoint or field, then add tests in `library-api/tests/` and run `make test` and `make check` until the pipeline is green.
4. **Teach Cursor**: Point Cursor at [AGENTS.md](AGENTS.md). It tells the AI to run `make check` before committing so changes are always tested and checked.

Config lives in **`pyproject.toml`** (Ruff, Radon, mypy, pytest). Adjust thresholds or rules there to match your tutorial or team standards.
