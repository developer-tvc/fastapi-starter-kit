from fastapi import HTTPException

from app.modules.roles.adapters.models import (PermissionModel, RoleModel,
                                               RolePermissionModel,
                                               UserRoleModel)
from app.modules.roles.entities.repositories import RoleRepository


class SQLAlchemyRoleRepository(RoleRepository):

    def __init__(self, db):
        self.db = db

    def get_user_permissions(self, user_id: int):

        permissions = (
            self.db.query(PermissionModel.name)
            .join(
                RolePermissionModel,
                PermissionModel.id == RolePermissionModel.permission_id,
            )
            .join(UserRoleModel, RolePermissionModel.role_id == UserRoleModel.role_id)
            .filter(UserRoleModel.user_id == user_id)
            .all()
        )

        return [p[0] for p in permissions]

    def create_permission(self, name: str):
        permission = PermissionModel(name=name)

        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)

        return permission

    def list_permissions(self):
        return self.db.query(PermissionModel).all()

    def update_permissions(self, permission_id: int, name: str):
        permission = (
            self.db.query(PermissionModel)
            .filter(PermissionModel.id == permission_id)
            .first()
        )
        if permission:
            permission.name = name
            self.db.commit()
            self.db.refresh(permission)
        return permission

    def delete_permissions(self, permission_id: int):
        permission = (
            self.db.query(PermissionModel)
            .filter(PermissionModel.id == permission_id)
            .first()
        )
        if permission:
            self.db.delete(permission)
            self.db.commit()
        return permission

    def create_role(self, name: str, description: str | None = None):
        role = RoleModel(name=name, description=description)

        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)

        return role

    def list_roles(self):
        return self.db.query(RoleModel).all()

    def update_role(self, role_id: int, name: str, description: str | None = None):
        role = self.db.query(RoleModel).filter(RoleModel.id == role_id).first()
        if role:
            role.name = name
            role.description = description
            self.db.commit()
            self.db.refresh(role)
        return role

    def delete_role(self, role_id: int):
        role = self.db.query(RoleModel).filter(RoleModel.id == role_id).first()
        if role:
            self.db.delete(role)
            self.db.commit()
        return role

    def assign_permission(self, role_id: int, permission_id: int):

        # check permission exists
        permission = (
            self.db.query(PermissionModel)
            .filter(PermissionModel.id == permission_id)
            .first()
        )

        if not permission:
            return None

        # check if already assigned
        existing = (
            self.db.query(RolePermissionModel)
            .filter(
                RolePermissionModel.role_id == role_id,
                RolePermissionModel.permission_id == permission_id,
            )
            .first()
        )

        if existing:
            return existing

        # create new mapping
        role_permission = RolePermissionModel(
            role_id=role_id,
            permission_id=permission_id,
        )

        self.db.add(role_permission)
        self.db.commit()

        return role_permission

    def unassign_permission(self, role_id: int, permission_id: int):

        permission = (
            self.db.query(PermissionModel)
            .filter(PermissionModel.id == permission_id)
            .first()
        )

        if not permission:
            raise HTTPException(status_code=404, detail="Permission not found")

        existing = (
            self.db.query(RolePermissionModel)
            .filter(
                RolePermissionModel.role_id == role_id,
                RolePermissionModel.permission_id == permission_id,
            )
            .first()
        )

        if not existing:
            raise HTTPException(
                status_code=404, detail="Permission not assigned to role"
            )

        removed = existing

        self.db.delete(existing)
        self.db.commit()

        return removed

    def get_user_permissions(self, user_id: int):
        permissions = (
            self.db.query(PermissionModel.name)
            .join(
                RolePermissionModel,
                PermissionModel.id == RolePermissionModel.permission_id,
            )
            .join(UserRoleModel, RolePermissionModel.role_id == UserRoleModel.role_id)
            .filter(UserRoleModel.user_id == user_id)
            .all()
        )

        return [p[0] for p in permissions]

    def assign_role(self, user_id: int, role_id: int):
        role = self.db.query(RoleModel).filter(RoleModel.id == role_id).first()

        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        existing = (
            self.db.query(UserRoleModel)
            .filter(
                UserRoleModel.user_id == user_id,
                UserRoleModel.role_id == role_id,
            )
            .first()
        )

        if existing:
            return existing

        user_role = UserRoleModel(
            user_id=user_id,
            role_id=role_id,
        )

        self.db.add(user_role)
        self.db.commit()

        return user_role

    def unassign_role(self, user_id: int, role_id: int):
        role = self.db.query(RoleModel).filter(RoleModel.id == role_id).first()

        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        existing = (
            self.db.query(UserRoleModel)
            .filter(
                UserRoleModel.user_id == user_id,
                UserRoleModel.role_id == role_id,
            )
            .first()
        )

        if not existing:
            raise HTTPException(status_code=404, detail="Role not assigned to user")

        removed = existing

        self.db.delete(existing)
        self.db.commit()

        return removed
