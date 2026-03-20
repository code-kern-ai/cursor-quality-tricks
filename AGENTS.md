# Agent instructions – cursor-quality-tricks

This repo is a **tutorial for code quality and automated testing** intended to work with Cursor. All quality checks and tests are run via a single Makefile so that Cursor (and humans) can validate changes before committing.

## Project overview

- **Book Library API**: FastAPI CRUD app in `library-api/` with SQLite and a minimal web UI.
- **Run the app**: `pip install -r requirements.txt` (or `-r library-api/requirements.txt`) then `python run.py`. Open http://127.0.0.1:8100.

## Quality and testing (required before commit)

**Always run `make check` (or `make all`) before committing or pushing. Do not commit if it fails.**

### Commands (run from repo root)

| Command        | Description                                      |
|----------------|--------------------------------------------------|
| `make check`   | Full pipeline: lint, format, typecheck, quality, test |
| `make all`     | Same as `make check`                             |
| `make test`    | Run pytest                                       |
| `make lint`    | Ruff lint                                       |
| `make format`  | Ruff format                                     |
| `make quality` | Radon cyclomatic complexity + maintainability   |
| `make typecheck` | mypy type checking                            |

### First-time setup

```bash
pip install -r requirements-dev.txt
```

(Same as `-r library-api/requirements-dev.txt`.)

### What each step does

- **lint**: Ruff checks style and common issues.
- **format**: Ruff formats code (run this to fix formatting).
- **typecheck**: mypy checks types in `library-api/`.
- **quality**: Radon reports cyclomatic complexity and maintainability index.
- **test**: Pytest runs unit and API tests in `library-api/tests/`.

### Adding tests

- Unit/CRUD tests: `library-api/tests/test_crud.py`
- API endpoint tests: `library-api/tests/test_api.py`
- Model validation tests: `library-api/tests/test_models.py`
- Shared fixtures (DB, client): `library-api/tests/conftest.py`

Add new test modules or test functions following the same patterns. Keep tests fast and isolated (in-memory SQLite per test).

### Fixing common issues

- **Ruff**: Run `make format` and fix any remaining lint errors reported by `make lint`.
- **mypy**: Add type hints or correct types; use `# type: ignore` only when necessary and documented.
- **Radon**: Refactor functions with high cyclomatic complexity or low maintainability (e.g. split into smaller functions).
- **pytest**: Ensure no tests are skipped and all pass; fix failing tests before committing.
