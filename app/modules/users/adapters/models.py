from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.modules.activity_logs.audit_mixin import AuditModelMixin


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    full_name = Column(String(100), nullable=True)
    phone = Column(String(15), nullable=True)
    profile_picture = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    roles = relationship(
        "UserRoleModel", back_populates="user", cascade="all, delete-orphan"
    )
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    is_locked = Column(Boolean, default=False)
    locked_until = Column(DateTime, nullable=True)
    last_failed_login_at = Column(DateTime, nullable=True)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 