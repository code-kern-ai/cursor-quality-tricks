"""Tests for Pydantic models (validation)."""

import pytest
from pydantic import ValidationError

from models import Book, BookCreate, BookUpdate


def test_book_create_valid():
    """BookCreate accepts valid data."""
    b = BookCreate(
        title="Valid Title",
        author="Author",
        genre="Fiction",
        year_published=2000,
        is_available=True,
    )
    assert b.title == "Valid Title"
    assert b.year_published == 2000


def test_book_create_title_min_length():
    """BookCreate rejects empty title."""
    with pytest.raises(ValidationError):
        BookCreate(
            title="",
            author="Author",
            genre="Fiction",
            year_published=2000,
            is_available=True,
        )


def test_book_create_year_bounds():
    """BookCreate rejects year outside 1000-2100."""
    with pytest.raises(ValidationError):
        BookCreate(
            title="Title",
            author="Author",
            genre="Fiction",
            year_published=999,
            is_available=True,
        )
    with pytest.raises(ValidationError):
        BookCreate(
            title="Title",
            author="Author",
            genre="Fiction",
            year_published=2101,
            is_available=True,
        )


def test_book_update_all_optional():
    """BookUpdate allows all fields optional."""
    b = BookUpdate()
    assert b.title is None
    assert b.author is None
    assert b.is_available is None


def test_book_update_partial():
    """BookUpdate accepts partial data."""
    b = BookUpdate(title="New Title", author=None, genre=None, year_published=None, is_available=None)
    assert b.title == "New Title"


def test_book_update_year_bounds():
    """BookUpdate validates year when provided."""
    with pytest.raises(ValidationError):
        BookUpdate(
            title=None,
            author=None,
            genre=None,
            year_published=500,
            is_available=None,
        )


def test_book_response_requires_id():
    """Book (response model) requires id."""
    with pytest.raises(ValidationError):
        Book(
            title="T",
            author="A",
            genre="G",
            year_published=2000,
            is_available=True,
        )
    b = Book(
        id=1,
        title="T",
        author="A",
        genre="G",
        year_published=2000,
        is_available=True,
    )
    assert b.id == 1
