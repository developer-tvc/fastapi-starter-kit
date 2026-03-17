"""
Dependencies are functions that are called by the router.
They are used to get the database session and the current user.
"""
from typing import Generator
from sqlalchemy.orm import Session
from app.core.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Returns a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
