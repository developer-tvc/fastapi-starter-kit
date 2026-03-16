from fastapi import APIRouter
from app.core.database import SessionLocal
from sqlalchemy import text

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/ready")
def ready_check():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()

        return {"status": "ready", "database": "connected"}

    except Exception:

        return {"status": "not_ready", "database": "disconnected"}
