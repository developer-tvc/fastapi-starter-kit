from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.schemas.response import APIResponse
from app.core.security import require_permission
from app.modules.roles import constants
from app.modules.roles.adapters.sqlalchemy_repository import SQLAlchemyRoleRepository
from app.modules.roles.controllers import schemas
from app.modules.roles.services.assign_permission import AssignPermission
from app.modules.roles.services.assign_role import AssignRole
from app.modules.roles.services.create_permission import CreatePermission
from app.modules.roles.services.create_role import CreateRole
from app.modules.roles.services.delete_permission import DeletePermission
from app.modules.roles.services.delete_role import DeleteRole
from app.modules.roles.services.get_user_permissions import GetUserPermissions
from app.modules.roles.services.list_permissions import ListPermissions
from app.modules.roles.services.list_role import ListRoles
from app.modules.roles.services.unassign_permission import UnassignPermission
from app.modules.roles.services.unassign_role import UnassignRole
from app.modules.roles.services.update_permissions import UpdatePermissions
from app.modules.roles.services.update_role import UpdateRole

router = APIRouter(
    tags=["Permissions Management"],
)


@router.post("/permissions", response_model=APIResponse[schemas.PermissionResponse])
async def create_permission(
    permission: schemas.PermissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission(constants.PERMISSION_CREATE)),
):
    repo = SQLAlchemyRoleRepository(db)
    service = CreatePermission(repo)
    result = await service.execute(permission.name)
    return APIResponse.success_response(
        data=result, message="Permission created successfully"
    )


@router.get(
    "/permissions", response_model=APIResponse[list[schemas.PermissionResponse]]
)
async def list_permissions(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission(constants.PERMISSION_VIEW)),
):
    repo = SQLAlchemyRoleRepository(db)
    service = ListPermissions(repo)
    result = await service.execute()

    return APIResponse.success_response(
        data=result, message="Permissions fetched successfully"
    )


@router.put(
    "/permissions", response_model=APIResponse[schemas.PermissionUpdateResponse]
)
async def update_permissions(
    permission_id: int,
    permission: schemas.PermissionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission(constants.PERMISSION_UPDATE)),
):
    repo = SQLAlchemyRoleRepository(db)
    service = UpdatePermissions(repo)
    result = await service.execute(permission_id, permission.name)

    return APIResponse.success_response(
        data=result, message="Permission updated successfully"
    )


@router.delete(
    "/permissions", response_model=APIResponse[schemas.PermissionDeleteResponse]
)
async def delete_permissions(
    permission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission(constants.PERMISSION_UPDATE)),
):
    repo = SQLAlchemyRoleRepository(db)
    service = DeletePermission(repo)
    result = await service.execute(permission_id)
    return APIResponse.success_response(
        data=result, message="Permission deleted successfully"
    )


@router.post("/roles", response_model=APIResponse[schemas.RoleResponse])
async def create_role(
    role: schemas.RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission(constants.ROLE_CREATE)),
):
    repo = SQLAlchemyRoleRepository(db)
    service = CreateRole(repo)
    result = await service.execute(role.name, role.description)
    return APIResponse.success_response(
        data=result, message="Role created successfully"
    )


@router.get("/roles", response_model=APIResponse[list[schemas.RoleResponse]])
async def list_roles(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission(constants.ROLE_VIEW)),
):
    repo = SQLAlchemyRoleRepository(db)
    service = ListRoles(repo)
    result = await service.execute()
    return APIResponse.success_response(
        data=result, message="Roles fetched successfully"
    )


@router.put("/roles", response_model=APIResponse[schemas.RoleUpdateResponse])
async def update_role(
    role_id: int,
    role: schemas.RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission(constants.ROLE_UPDATE)),
):
    repo = SQLAlchemyRoleRepository(db)
    service = UpdateRole(repo)
    result = await service.execute(role_id, role.name, role.description)
    return APIResponse.success_response(
        data=result, message="Role updated successfully"
    )


@router.delete("/roles", response_model=APIResponse[schemas.RoleDeleteResponse])
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission(constants.ROLE_UPDATE)),
):
    repo = SQLAlchemyRoleRepository(db)
    service = DeleteRole(repo)
    result = await service.execute(role_id)
    return APIResponse.success_response(
        data=result, message="Role deleted successfully"
    )


@router.post("/assign_permission", response_model=APIResponse[schemas.AssignPermission])
async def assign_permission(
    role_id: int,
    permission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission(constants.ASSIGN_PERMISSION)),
):
    repo = SQLAlchemyRoleRepository(db)
    service = AssignPermission(repo)
    result = await service.execute(role_id, permission_id)
    return APIResponse.success_response(
        data=result, message="Permission assigned successfully"
    )


@router.delete(
    "/unassign_permission", response_model=APIResponse[schemas.AssignPermission]
)
async def unassign_permission(
    role_id: int,
    permission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission(constants.UNASSIGN_PERMISSION)),
):
    repo = SQLAlchemyRoleRepository(db)
    service = UnassignPermission(repo)
    result = await service.execute(role_id, permission_id)
    return APIResponse.success_response(
        data=result, message="Permission unassigned successfully"
    )


@router.get("/user_permissions", response_model=APIResponse[list[str]])
async def get_user_permissions(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission(constants.USER_PERMISSION)),
):
    repo = SQLAlchemyRoleRepository(db)
    service = GetUserPermissions(repo)
    result = await service.execute(user_id)
    return APIResponse.success_response(
        data=result, message="User Permission fetched successfully"
    )


@router.post("/assign_role", response_model=APIResponse[schemas.AssignRoleToUser])
async def assign_role(
    assign_req: schemas.AssignRoleToUser,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission(constants.ASSIGN_ROLE)),
):
    repo = SQLAlchemyRoleRepository(db)
    service = AssignRole(repo)
    result = await service.execute(assign_req.user_id, assign_req.role_id)
    return APIResponse.success_response(
        data=result, message="User role assigned successfully"
    )


@router.delete("/assign_role", response_model=APIResponse[schemas.AssignRoleToUser])
async def unassign_role(
    user_id: int,
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission(constants.UNASSIGN_ROLE)),
):
    repo = SQLAlchemyRoleRepository(db)
    service = UnassignRole(repo)
    result = await service.execute(user_id, role_id)
    return APIResponse.success_response(
        data=result, message="User role unassigned successfully"
    )
