"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_list_books_empty(client: TestClient):
    """GET /api/books returns empty list when no books."""
    r = client.get("/api/books")
    assert r.status_code == 200
    assert r.json() == []


def test_create_book(client: TestClient):
    """POST /api/books creates a book and returns it."""
    payload = {
        "title": "New Book",
        "author": "Jane Doe",
        "genre": "Mystery",
        "year_published": 2023,
        "is_available": True,
    }
    r = client.post("/api/books", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "New Book"
    assert data["author"] == "Jane Doe"
    assert "id" in data


def test_get_book(client: TestClient):
    """GET /api/books/{id} returns a single book."""
    create_r = client.post(
        "/api/books",
        json={
            "title": "One Book",
            "author": "Author",
            "genre": "Fiction",
            "year_published": 2020,
            "is_available": True,
        },
    )
    book_id = create_r.json()["id"]
    r = client.get(f"/api/books/{book_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "One Book"


def test_get_book_not_found(client: TestClient):
    """GET /api/books/{id} returns 404 for missing ID."""
    r = client.get("/api/books/99999")
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


def test_update_book(client: TestClient):
    """PUT /api/books/{id} updates a book (partial update)."""
    create_r = client.post(
        "/api/books",
        json={
            "title": "Original",
            "author": "Author",
            "genre": "Fiction",
            "year_published": 2020,
            "is_available": True,
        },
    )
    book_id = create_r.json()["id"]
    r = client.put(f"/api/books/{book_id}", json={"title": "Updated"})
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Updated"
    assert data["author"] == "Author"


def test_update_book_not_found(client: TestClient):
    """PUT /api/books/{id} returns 404 for missing ID."""
    r = client.put("/api/books/99999", json={"title": "No"})
    assert r.status_code == 404


def test_delete_book(client: TestClient):
    """DELETE /api/books/{id} removes the book."""
    create_r = client.post(
        "/api/books",
        json={
            "title": "To Delete",
            "author": "Author",
            "genre": "Fiction",
            "year_published": 2020,
            "is_available": True,
        },
    )
    book_id = create_r.json()["id"]
    r = client.delete(f"/api/books/{book_id}")
    assert r.status_code == 204
    get_r = client.get(f"/api/books/{book_id}")
    assert get_r.status_code == 404


def test_delete_book_not_found(client: TestClient):
    """DELETE /api/books/{id} returns 404 for missing ID."""
    r = client.delete("/api/books/99999")
    assert r.status_code == 404


def test_create_book_validation_fails(client: TestClient):
    """POST /api/books returns 422 for invalid payload."""
    r = client.post(
        "/api/books",
        json={
            "title": "",
            "author": "Author",
            "genre": "Fiction",
            "year_published": 999,
            "is_available": True,
        },
    )
    assert r.status_code == 422
