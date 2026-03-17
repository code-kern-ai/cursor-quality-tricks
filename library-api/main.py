"""FastAPI Book Library API - A tutorial CRUD application."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine, get_db
from schemas import BookORM
from models import Book, BookCreate, BookUpdate
from crud import (
    get_books as crud_get_books,
    get_book as crud_get_book,
    create_book as crud_create_book,
    update_book as crud_update_book,
    delete_book as crud_delete_book,
)

# Create database tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Seed sample books on startup if database is empty."""
    db = SessionLocal()
    try:
        if db.query(BookORM).count() == 0:
            sample_books = [
                BookORM(title="The Great Gatsby", author="F. Scott Fitzgerald", genre="Fiction", year_published=1925, is_available=True),
                BookORM(title="1984", author="George Orwell", genre="Dystopian", year_published=1949, is_available=True),
                BookORM(title="To Kill a Mockingbird", author="Harper Lee", genre="Fiction", year_published=1960, is_available=False),
            ]
            for book in sample_books:
                db.add(book)
            db.commit()
    except Exception:
        pass
    finally:
        db.close()
    yield


app = FastAPI(
    title="Book Library API",
    description="A simple CRUD API for managing a book collection - perfect for tutorials!",
    version="1.0.0",
    lifespan=lifespan,
)

# Serve static files (UI)
static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


@app.get("/")
async def root():
    """Serve the web UI."""
    index_path = static_path / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Book Library API", "docs": "/docs"}


# --- CRUD Endpoints ---


@app.get("/api/books", response_model=list[Book])
def list_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all books with optional pagination."""
    return crud_get_books(db, skip=skip, limit=limit)


@app.get("/api/books/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Get a single book by ID."""
    book = crud_get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/api/books", response_model=Book, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Create a new book."""
    return crud_create_book(db, book)


@app.put("/api/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    """Update an existing book."""
    updated = crud_update_book(db, book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated


@app.delete("/api/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book."""
    if not crud_delete_book(db, book_id):
        raise HTTPException(status_code=404, detail="Book not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8100, reload=True)
