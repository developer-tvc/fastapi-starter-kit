from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base


class NotificationModel(Base):

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    message = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class NotificationLogModel(Base):

    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    title = Column(String)
    message = Column(String)

    channel = Column(String)  # email / sms / inapp / webhook

    status = Column(String, default="pending")
    # pending | sent | failed

    error_message = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
