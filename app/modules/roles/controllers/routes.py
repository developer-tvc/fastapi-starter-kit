from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.security import require_permission

from app.modules.roles.controllers import schemas
from app.modules.roles.adapters.sqlalchemy_repository import SQLAlchemyRoleRepository
from app.modules.roles.services.create_permission import CreatePermission
from app.modules.roles.services.list_permissions import ListPermissions
from app.modules.roles.services.update_permissions import UpdatePermissions
from app.modules.roles.services.delete_permission import DeletePermission
from app.modules.roles.services.create_role import CreateRole
from app.modules.roles.services.list_role import ListRoles
from app.modules.roles.services.update_role import UpdateRole
from app.modules.roles.services.delete_role import DeleteRole

router = APIRouter(
    
    tags=["Permissions Management"],
)

@router.post("/permissions", response_model=schemas.PermissionResponse)
def create_permission(
    permission: schemas.PermissionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("permission:create"))
):
    repo = SQLAlchemyRoleRepository(db)
    service = CreatePermission(repo)

    return service.execute(permission.name)



@router.get("/permissions", response_model=list[schemas.PermissionResponse])
def list_permissions(
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("permission:view"))
):
    repo = SQLAlchemyRoleRepository(db)
    service = ListPermissions(repo)

    return service.execute()


@router.put("/permissions", response_model=schemas.PermissionUpdateResponse)
def update_permissions(
    permission_id: int,
    permission: schemas.PermissionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("permission:update"))
):
    repo = SQLAlchemyRoleRepository(db)
    service = UpdatePermissions(repo)

    return service.execute(permission_id, permission.name)



@router.delete("/permissions", response_model=schemas.PermissionDeleteResponse)
def delete_permissions(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("permission:update"))
):
    repo = SQLAlchemyRoleRepository(db)
    service = DeletePermission(repo)

    return service.execute(permission_id)

@router.post("/roles", response_model=schemas.RoleResponse)
def create_role(
    role: schemas.RoleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("role:create"))
):
    repo = SQLAlchemyRoleRepository(db)
    service = CreateRole(repo)

    return service.execute(role.name, role.description)


@router.get("/roles", response_model=list[schemas.RoleResponse])
def list_roles(
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("role:view"))
):
    repo = SQLAlchemyRoleRepository(db)
    service = ListRoles(repo)

    return service.execute()

@router.put("/roles", response_model=schemas.RoleUpdateResponse)
def update_role(
    role_id: int,
    role: schemas.RoleUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("role:update"))
):
    repo = SQLAlchemyRoleRepository(db)
    service = UpdateRole(repo)

    return service.execute(role_id, role.name, role.description)

@router.delete("/roles", response_model=schemas.RoleDeleteResponse)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("role:update"))
):
    repo = SQLAlchemyRoleRepository(db)
    service = DeleteRole(repo)

    return service.execute(role_id)

    
