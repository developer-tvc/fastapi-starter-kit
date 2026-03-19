from fastapi import APIRouter
from app.core.database import AsyncSessionLocal
from sqlalchemy import text

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/ready")
async def ready_check():
    try:
        async with AsyncSessionLocal() as db:
            await db.execute(text("SELECT 1"))

        return {"status": "ready", "database": "connected"}

    except Exception:

        return {"status": "not_ready", "database": "disconnected"}
