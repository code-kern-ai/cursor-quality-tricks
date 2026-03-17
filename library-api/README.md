# Book Library API – FastAPI CRUD Tutorial

A simple **Book Library** application demonstrating full CRUD operations with FastAPI, SQLite, and a minimal web UI.

## Domain: Book Library

- **Books** have: title, author, genre, year published, and availability status
- Perfect for learning: Create, Read, Update, Delete patterns

## Quick Start

From the project root:

```bash
pip install -r library-api/requirements.txt
python run.py
```

Or from this directory:

```bash
pip install -r requirements.txt
python main.py
```

Open **http://127.0.0.1:8100** for the web UI, or **http://127.0.0.1:8100/docs** for the interactive API docs. If port 8100 is in use, stop the existing server first.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/books` | List all books |
| GET | `/api/books/{id}` | Get one book |
| POST | `/api/books` | Create a book |
| PUT | `/api/books/{id}` | Update a book |
| DELETE | `/api/books/{id}` | Delete a book |

## Project Structure

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
