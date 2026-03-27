from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.roles.adapters.models import (
    PermissionModel,
    RoleModel,
    RolePermissionModel,
    UserRoleModel,
)
from app.modules.roles.entities.repositories import RoleRepository


class SQLAlchemyRoleRepository(RoleRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_permissions(self, user_id: int):

        stmt = (
            select(PermissionModel.name)
            .join(
                RolePermissionModel,
                PermissionModel.id == RolePermissionModel.permission_id,
            )
            .join(UserRoleModel, RolePermissionModel.role_id == UserRoleModel.role_id)
            .where(UserRoleModel.user_id == user_id)
        )

        result = await self.db.execute(stmt)
        permissions = result.all()

        return [p[0] for p in permissions]

    async def create_permission(self, name: str):
        permission = PermissionModel(name=name)

        self.db.add(permission)
        await self.db.commit()
        await self.db.refresh(permission)

        return permission

    async def list_permissions(self):
        result = await self.db.execute(select(PermissionModel))
        return result.scalars().all()

    async def update_permissions(self, permission_id: int, name: str):
        result = await self.db.execute(
            select(PermissionModel).where(PermissionModel.id == permission_id)
        )
        permission = result.scalar_one_or_none()

        if permission:
            permission.name = name
            await self.db.commit()
            await self.db.refresh(permission)
        return permission

    async def delete_permissions(self, permission_id: int):
        result = await self.db.execute(
            select(PermissionModel).where(PermissionModel.id == permission_id)
        )
        permission = result.scalar_one_or_none()

        if permission:
            await self.db.delete(permission)
            await self.db.commit()
        return permission

    async def create_role(self, name: str, description: str | None = None):
        role = RoleModel(name=name, description=description)

        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)

        return role

    async def list_roles(self):
        result = await self.db.execute(select(RoleModel))
        return result.scalars().all()

    async def update_role(
        self, role_id: int, name: str, description: str | None = None
    ):
        result = await self.db.execute(select(RoleModel).where(RoleModel.id == role_id))
        role = result.scalar_one_or_none()

        if role:
            role.name = name
            role.description = description
            await self.db.commit()
            await self.db.refresh(role)
        return role

    async def delete_role(self, role_id: int):
        result = await self.db.execute(select(RoleModel).where(RoleModel.id == role_id))
        role = result.scalar_one_or_none()

        if role:
            await self.db.delete(role)
            await self.db.commit()
        return role

    async def assign_permission(self, role_id: int, permission_id: int):

        # check permission exists
        result = await self.db.execute(
            select(PermissionModel).where(PermissionModel.id == permission_id)
        )
        permission = result.scalar_one_or_none()

        if not permission:
            return None

        # check if already assigned
        result = await self.db.execute(
            select(RolePermissionModel).where(
                RolePermissionModel.role_id == role_id,
                RolePermissionModel.permission_id == permission_id,
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            return existing

        # create new mapping
        role_permission = RolePermissionModel(
            role_id=role_id,
            permission_id=permission_id,
        )

        self.db.add(role_permission)
        await self.db.commit()

        return role_permission

    async def unassign_permission(self, role_id: int, permission_id: int):

        result = await self.db.execute(
            select(PermissionModel).where(PermissionModel.id == permission_id)
        )
        permission = result.scalar_one_or_none()

        if not permission:
            raise HTTPException(status_code=404, detail="Permission not found")

        result = await self.db.execute(
            select(RolePermissionModel).where(
                RolePermissionModel.role_id == role_id,
                RolePermissionModel.permission_id == permission_id,
            )
        )
        existing = result.scalar_one_or_none()

        if not existing:
            raise HTTPException(
                status_code=404, detail="Permission not assigned to role"
            )

        removed = existing

        await self.db.delete(existing)
        await self.db.commit()

        return removed

    async def assign_role(self, user_id: int, role_id: int):
        result = await self.db.execute(select(RoleModel).where(RoleModel.id == role_id))
        role = result.scalar_one_or_none()

        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        result = await self.db.execute(
            select(UserRoleModel).where(
                UserRoleModel.user_id == user_id,
                UserRoleModel.role_id == role_id,
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            return existing

        user_role = UserRoleModel(
            user_id=user_id,
            role_id=role_id,
        )

        self.db.add(user_role)
        await self.db.commit()

        return user_role

    async def unassign_role(self, user_id: int, role_id: int):
        result = await self.db.execute(select(RoleModel).where(RoleModel.id == role_id))
        role = result.scalar_one_or_none()

        if not role:
            raise HTTPException(status_code=404, detail="Role not found")

        result = await self.db.execute(
            select(UserRoleModel).where(
                UserRoleModel.user_id == user_id,
                UserRoleModel.role_id == role_id,
            )
        )
        existing = result.scalar_one_or_none()

        if not existing:
            raise HTTPException(status_code=404, detail="Role not assigned to user")

        removed = existing

        await self.db.delete(existing)
        await self.db.commit()

        return removed
