from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.modules.activity_logs.audit_mixin import AuditModelMixin


class UserRoleModel(AuditModelMixin, Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    user = relationship("UserModel", back_populates="roles")
    role = relationship("RoleModel")


class RoleModel(AuditModelMixin, Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    permissions = relationship("RolePermissionModel", back_populates="role")


class PermissionModel(AuditModelMixin, Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    roles = relationship("RolePermissionModel", back_populates="permission")


class RolePermissionModel(AuditModelMixin, Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True)

    role_id = Column(Integer, ForeignKey("roles.id"))
    permission_id = Column(Integer, ForeignKey("permissions.id"))

    role = relationship("RoleModel", back_populates="permissions")
    permission = relationship("PermissionModel", back_populates="roles")
