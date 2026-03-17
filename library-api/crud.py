"""CRUD operations for the Book Library."""

from sqlalchemy.orm import Session

from schemas import BookORM
from models import BookCreate, BookUpdate


def get_books(db: Session, skip: int = 0, limit: int = 100):
    """Get all books with optional pagination."""
    return db.query(BookORM).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int):
    """Get a single book by ID."""
    return db.query(BookORM).filter(BookORM.id == book_id).first()


def create_book(db: Session, book: BookCreate):
    """Create a new book."""
    db_book = BookORM(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: BookUpdate):
    """Update an existing book."""
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    update_data = book.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    """Delete a book."""
    db_book = get_book(db, book_id)
    if not db_book:
        return False
    db.delete(db_book)
    db.commit()
    return True
