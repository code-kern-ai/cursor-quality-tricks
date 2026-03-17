"""Tests for CRUD operations."""

import pytest

from crud import create_book, delete_book, get_book, get_books, update_book
from models import BookCreate, BookUpdate


def test_get_books_empty(db_session):
    """List books when database is empty."""
    assert get_books(db_session) == []


def test_create_and_get_book(db_session):
    """Create a book and retrieve it by ID."""
    book_in = BookCreate(
        title="Test Book",
        author="Test Author",
        genre="Fiction",
        year_published=2020,
        is_available=True,
    )
    created = create_book(db_session, book_in)
    assert created.id is not None
    assert created.title == "Test Book"
    assert created.author == "Test Author"

    fetched = get_book(db_session, created.id)
    assert fetched is not None
    assert fetched.title == created.title
    assert fetched.id == created.id


def test_get_books_with_pagination(db_session):
    """List books with skip and limit."""
    for i in range(5):
        create_book(
            db_session,
            BookCreate(
                title=f"Book {i}",
                author="Author",
                genre="Fiction",
                year_published=2000 + i,
                is_available=True,
            ),
        )
    all_books = get_books(db_session)
    assert len(all_books) == 5

    page1 = get_books(db_session, skip=0, limit=2)
    assert len(page1) == 2
    assert page1[0].title == "Book 0"

    page2 = get_books(db_session, skip=2, limit=2)
    assert len(page2) == 2
    assert page2[0].title == "Book 2"


def test_get_book_not_found(db_session):
    """get_book returns None for missing ID."""
    assert get_book(db_session, 99999) is None


def test_update_book(db_session):
    """Update an existing book (partial update: only title)."""
    created = create_book(
        db_session,
        BookCreate(
            title="Original",
            author="Author",
            genre="Fiction",
            year_published=2020,
            is_available=True,
        ),
    )
    updated = update_book(db_session, created.id, BookUpdate(title="Updated Title"))
    assert updated is not None
    assert updated.title == "Updated Title"
    assert updated.author == "Author"

    fetched = get_book(db_session, created.id)
    assert fetched.title == "Updated Title"


def test_update_book_not_found(db_session):
    """update_book returns None for missing ID."""
    result = update_book(db_session, 99999, BookUpdate(title="No"))
    assert result is None


def test_delete_book(db_session):
    """Delete a book."""
    created = create_book(
        db_session,
        BookCreate(
            title="To Delete",
            author="Author",
            genre="Fiction",
            year_published=2020,
            is_available=True,
        ),
    )
    assert delete_book(db_session, created.id) is True
    assert get_book(db_session, created.id) is None


def test_delete_book_not_found(db_session):
    """delete_book returns False for missing ID."""
    assert delete_book(db_session, 99999) is False
