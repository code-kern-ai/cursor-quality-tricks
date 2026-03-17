"""SQLAlchemy ORM model for the books table."""

from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class BookORM(Base):
    """SQLAlchemy model for the books table."""

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    author = Column(String(100), index=True)
    genre = Column(String(50))
    year_published = Column(Integer)
    is_available = Column(Boolean, default=True)
