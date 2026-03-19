from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.modules.auth.services.user_login import LoginUserService
from app.modules.users.adapters.sqlalchemy_repository import SQLAlchemyUserRepository
from app.modules.auth.controllers import schemas
from fastapi.security import OAuth2PasswordRequestForm
from app.modules.auth.services.refresh_token import RefreshTokenService
from app.modules.auth.controllers.schemas import RefreshRequest
from app.modules.auth.services.logout_user import LogoutUserService
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.modules.auth.adapters.blacklist_repository import BlacklistRepository
from app.core.schemas.response import APIResponse
from app.core.security import verify_password_reset_token, hash_password
from app.modules.auth.services.reset_password_request import ResetPasswordRequestService
from app.modules.auth.services.confirm_password_reset import ConfirmPasswordResetService
from app.modules.auth.services.verify_user import VerifyUserService
from app.core.security import verify_email_token
from fastapi import HTTPException, Request
from app.core.security import limiter
from app.modules.auth.services.register_device import RegisterDeviceService
from app.modules.auth.adapters.device_repository import DeviceRepository
from sqlalchemy.ext.asyncio import AsyncSession

security = HTTPBearer()

router = APIRouter(
    tags=["Auth"],
)


@router.post("/login")
@limiter.limit("5/minute")  # Rate Limiting
async def login(
    request: Request, body: schemas.LoginRequest, db: AsyncSession = Depends(get_db)
):
    repo = SQLAlchemyUserRepository(db)
    device_repo = DeviceRepository(db)  # Device Repository
    register_device_service = RegisterDeviceService(
        device_repo
    )  # Register Device Service
    service = LoginUserService(repo, register_device_service)
    return await service.execute(
        email=body.email, password=body.password, request=request
    )


# OAuth2 login (Swagger)
@router.post("/token")
async def login_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    repo = SQLAlchemyUserRepository(db)
    service = LoginUserService(repo, None)

    return await service.execute(
        email=form_data.username, password=form_data.password, request=request
    )


@router.post("/refresh")
async def refresh_token(request: RefreshRequest):

    service = RefreshTokenService()

    return await service.execute(request.refresh_token)


@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):

    token = credentials.credentials
    blacklist_repo = BlacklistRepository(db)
    service = LogoutUserService(blacklist_repo)

    return await service.execute(token)


@router.post("/password-reset/request", response_model=APIResponse[None])
async def request_password_reset(
    payload: schemas.PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),  
):
    repo = SQLAlchemyUserRepository(db)
    service = ResetPasswordRequestService(repo)

    await service.execute(payload, background_tasks)

    return APIResponse.success_response(
        message="If the email exists, a reset link has been sent"
    )


@router.post("/password-reset/confirm", response_model=APIResponse[None])
async def confirm_password_reset(
    payload: schemas.PasswordResetConfirm, db: AsyncSession = Depends(get_db)
):
    user_id = verify_password_reset_token(payload.token)

    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    hashed_password = hash_password(payload.new_password)
    repo = SQLAlchemyUserRepository(db)
    service = ConfirmPasswordResetService(repo)
    await service.execute(user_id, hashed_password)

    return APIResponse.success_response(message="Password reset successfully")


@router.post("/verify-email", response_model=APIResponse[None])
async def verify_email(
    payload: schemas.EmailVerificationRequest, db: AsyncSession = Depends(get_db)
):

    user_id = verify_email_token(payload.token)

    if not user_id:
        return APIResponse.error_response("Invalid or expired token")

    repo = SQLAlchemyUserRepository(db)
    service = VerifyUserService(repo)
    await service.execute(user_id)

    return APIResponse.success_response(message="Email verified successfully")
