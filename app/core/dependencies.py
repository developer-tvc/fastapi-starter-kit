"""
Dependencies are functions that are called by the router.
They are used to get the database session and the current user.
"""

from typing import Generator

from sqlalchemy.orm import Session

from app.core.database import AsyncSessionLocal


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
