"""Pydantic models for the Book Library API."""

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    """Base schema for book data."""

    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    genre: str = Field(..., min_length=1, max_length=50)
    year_published: int = Field(..., ge=1000, le=2100)
    is_available: bool = True


class BookCreate(BookBase):
    """Schema for creating a new book."""

    pass


class BookUpdate(BaseModel):
    """Schema for updating a book (all fields optional)."""

    title: str | None = Field(None, min_length=1, max_length=200)
    author: str | None = Field(None, min_length=1, max_length=100)
    genre: str | None = Field(None, min_length=1, max_length=50)
    year_published: int | None = Field(None, ge=1000, le=2100)
    is_available: bool | None = None


class Book(BookBase):
    """Schema for a book response (includes id)."""

    id: int

    model_config = {"from_attributes": True}
