from app.modules.users.services.create_users import CreateUser
from app.modules.users.controllers import schemas
from app.modules.users.adapters.sqlalchemy_repository import SQLAlchemyUserRepository
from app.modules.users.services.list_users import ListUsers
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.modules.users.entities.entities import User
from app.core.dependencies import get_db
from app.core.security import require_permission
from app.modules.users import constants
from app.core.schemas.response import APIResponse
from app.modules.users.services.get_user import GetUser
from app.modules.users.services.update_user import UpdateUser
from app.modules.users.services.delete_user import DeleteUser
from app.modules.notifications.repositories.notification_repository import (
    NotificationRepository,
)
from app.modules.notifications.services.notification_service import NotificationService
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from app.core.schemas.pagination import PaginatedResponse

router = APIRouter(
)


@router.get("/", response_model=PaginatedResponse[schemas.UserResponse])
async def read_users(
    request: Request, 
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),  # Async session
    current_user: User = Depends(require_permission(constants.VIEW_PERMISSION)),
):
    repo = SQLAlchemyUserRepository(db)  # Make sure repo methods are async
    use_case = ListUsers(repo)
    users,total = await use_case.execute(skip=skip, limit=limit)  # execute() must be async
    
    # Convert to response schema
    items = [schemas.UserResponse.model_validate(u) for u in users]

     # Build next & previous URLs
    def build_url(new_skip):
        return str(request.url.include_query_params(skip=new_skip, limit=limit))

    next_url = build_url(skip + limit) if skip + limit < total else None
    prev_url = build_url(skip - limit) if skip > 0 else None

    return PaginatedResponse(
            success=True,
            message="Users fetched successfully",
            total=total,
            next=next_url,
            previous=prev_url,
            data=items,
        )
        
 


@router.post("/", response_model=APIResponse[schemas.UserResponse])
async def create_user(
    user: schemas.UserCreate,  # Request body containing user data
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),  # Async DB session
    current_user: User = Depends(require_permission(constants.CREATE_PERMISSION)),
):
    repo = SQLAlchemyUserRepository(db)  # Make repo methods async
    notification_repo = NotificationRepository(db)  # Make repo methods async
    notification_service = NotificationService(notification_repo)
    use_case = CreateUser(repo, notification_service)  # Async use case
    
    created_user = await use_case.execute(
        user.email,
        user.password,
        user.full_name,
        user.roles,
        background_tasks,
        current_user,
    )

    return APIResponse.success_response(
        created_user, "User created successfully"
    )

@router.get("/profile", response_model=APIResponse[schemas.UserResponse])
async def get_me(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission(constants.VIEW_PERMISSION)),
):
    repo = SQLAlchemyUserRepository(db)  # Make repository methods async
    use_case = GetUser(repo)
    user_data = await use_case.execute(current_user.id)  # await DB call
    return APIResponse.success_response(
        data=user_data,
        message="User fetched successfully",
    )


@router.patch("/profile", response_model=APIResponse[schemas.UserProfileResponse])
async def update_profile(
    user: schemas.UserProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission(constants.UPDATE_PERMISSION)),
):
    repo = SQLAlchemyUserRepository(db)
    use_case = UpdateUser(repo)
    updated_user = await use_case.execute(current_user.id, user)  # await DB call
    return APIResponse.success_response(
        data=updated_user,
        message="User updated successfully",
    )


@router.get("/{user_id}", response_model=APIResponse[schemas.UserResponse])
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission(constants.VIEW_PERMISSION)),
):
    repo = SQLAlchemyUserRepository(db)
    use_case = GetUser(repo)
    user_data = await use_case.execute(user_id)  # await DB call
    return APIResponse.success_response(
        data=user_data,
        message="User fetched successfully",
    )


@router.put("/{user_id}", response_model=APIResponse[schemas.UserResponse])
async def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission(constants.UPDATE_PERMISSION)),
):
    repo = SQLAlchemyUserRepository(db)
    use_case = UpdateUser(repo)
    updated_user = await use_case.execute(user_id, user)  # await DB call
    return APIResponse.success_response(
        data=updated_user,
        message="User updated successfully",
    )


@router.delete("/{user_id}", response_model=APIResponse[None])
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission(constants.DELETE_PERMISSION)),
):
    repo = SQLAlchemyUserRepository(db)
    use_case = DeleteUser(repo)
    await use_case.execute(user_id)  # await DB call
    return APIResponse.success_response(
        data=None,
        message="User deleted successfully",
    )

