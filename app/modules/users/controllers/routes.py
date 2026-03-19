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

router = APIRouter(
)


@router.get("/", response_model=APIResponse[list[schemas.UserResponse]])
def read_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(constants.VIEW_PERMISSION)),
):
    repo = SQLAlchemyUserRepository(db)
    use_case = ListUsers(repo)
    return APIResponse.success_response(
        data=use_case.execute(),
        message="Users fetched successfully",
    )


@router.post("/", response_model=APIResponse[schemas.UserResponse])
def create_user(
    user: schemas.UserCreate,  # Request body containing user data
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),  # Inject database session
    current_user: User = Depends(require_permission(constants.CREATE_PERMISSION)),
):
    repo = SQLAlchemyUserRepository(db)  # User Repository
    notification_repo = NotificationRepository(db)  # Notification Repository
    notification_service = NotificationService(
        notification_repo
    )  # Notification Service
    use_case = CreateUser(repo, notification_service)  # Create User Use Case
    
    created_user = use_case.execute(
        user.email,
        user.password,
        user.full_name,
        user.roles,
        background_tasks,
        current_user,
    )

    return APIResponse.success_response(created_user, "User created successfully")



@router.get("/profile", response_model=APIResponse[schemas.UserResponse])
def get_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(constants.VIEW_PERMISSION)),
):
    repo = SQLAlchemyUserRepository(db)
    use_case = GetUser(repo)
    return APIResponse.success_response(
        data=use_case.execute(current_user.id),
        message="User fetched successfully",
    )


@router.patch("/profile", response_model=APIResponse[schemas.UserProfileResponse])
def update_profile(
    user: schemas.UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(constants.UPDATE_PERMISSION)),
):
    repo = SQLAlchemyUserRepository(db)
    use_case = UpdateUser(repo)
    return APIResponse.success_response(
        data=use_case.execute(current_user.id, user),
        message="User updated successfully",
    )


@router.get("/{user_id}", response_model=APIResponse[schemas.UserResponse])
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(constants.VIEW_PERMISSION)),
):
    repo = SQLAlchemyUserRepository(db)
    use_case = GetUser(repo)
    return APIResponse.success_response(
        data=use_case.execute(user_id),
        message="User fetched successfully",
    )


@router.put("/{user_id}", response_model=APIResponse[schemas.UserResponse])
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(constants.UPDATE_PERMISSION)),
):
    repo = SQLAlchemyUserRepository(db)
    use_case = UpdateUser(repo)
    return APIResponse.success_response(
        data=use_case.execute(user_id, user),
        message="User updated successfully",
    )


@router.delete("/{user_id}", response_model=APIResponse[None])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(constants.DELETE_PERMISSION)),
):
    repo = SQLAlchemyUserRepository(db)
    use_case = DeleteUser(repo)
    return APIResponse.success_response(
        data=use_case.execute(user_id),
        message="User deleted successfully",
    )
