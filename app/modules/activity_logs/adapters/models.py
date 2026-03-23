from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String

from app.db.base_class import Base


class ActivityLogModel(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    action = Column(String, nullable=False)

    object_type = Column(String, nullable=False)
    object_id = Column(Integer)

    ip_address = Column(String)

    old_value = Column(JSON)
    new_value = Column(JSON)

    description = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
