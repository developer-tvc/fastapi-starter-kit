from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime


class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    jti = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserDevice(Base):

    __tablename__ = "user_devices"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    device_id = Column(String, nullable=False)
    device_name = Column(String)
    user_agent = Column(String)

    ip_address = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, default=datetime.utcnow)
