from app.modules.roles.adapters.models import PermissionModel, RolePermissionModel, UserRoleModel, RoleModel
from app.modules.roles.entities.repositories import RoleRepository

class SQLAlchemyRoleRepository(RoleRepository):

    def __init__(self, db):
        self.db = db

    def get_user_permissions(self, user_id: int):

        permissions = (
            self.db.query(PermissionModel.name)
            .join(RolePermissionModel, PermissionModel.id == RolePermissionModel.permission_id)
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
        permission = self.db.query(PermissionModel).filter(PermissionModel.id == permission_id).first()
        if permission:
            permission.name = name
            self.db.commit()
            self.db.refresh(permission)
        return permission

    def delete_permissions(self, permission_id: int):
        permission = self.db.query(PermissionModel).filter(PermissionModel.id == permission_id).first()
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