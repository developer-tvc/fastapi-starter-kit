from fastapi import APIRouter, Depends,BackgroundTasks
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
from app.core.security import create_password_reset_token, verify_password_reset_token, hash_password
from app.core.services.email_service import send_email
from app.core.services.email_templates import password_reset_email
from app.modules.auth.services.reset_password_request import ResetPasswordRequestService
from app.modules.auth.services.confirm_password_reset import ConfirmPasswordResetService
from app.modules.auth.services.verify_user import VerifyUserService
from app.core.security import verify_email_token
from fastapi import HTTPException

security = HTTPBearer()

router = APIRouter(
    tags=["Auth"],
)

@router.post("/login")
async def login(
    request: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    repo = SQLAlchemyUserRepository(db)
    service = LoginUserService(repo)

    return await service.execute(
        email=request.email,
        password=request.password
    )


# OAuth2 login (Swagger)
@router.post("/token")
async def login_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    repo = SQLAlchemyUserRepository(db)
    service = LoginUserService(repo)

    return await service.execute(
        email=form_data.username,
        password=form_data.password
    )


@router.post("/refresh")
async def refresh_token(request: RefreshRequest):

    service = RefreshTokenService()

    return await service.execute(request.refresh_token)


@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials
    blacklist_repo = BlacklistRepository(db)
    service = LogoutUserService(blacklist_repo)

    return await service.execute(token)


@router.post("/password-reset/request", response_model=APIResponse[None])
def request_password_reset(
    payload: schemas.PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    repo = SQLAlchemyUserRepository(db)
    service = ResetPasswordRequestService(repo)
    
    service.execute(payload, background_tasks)
    

    return APIResponse.success_response(
        message="If the email exists, a reset link has been sent"
    )


@router.post("/password-reset/confirm", response_model=APIResponse[None])
def confirm_password_reset(
    payload: schemas.PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    user_id = verify_password_reset_token(payload.token)

    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired token"
        )
    hashed_password = hash_password(payload.new_password)
    repo = SQLAlchemyUserRepository(db)
    service = ConfirmPasswordResetService(repo)
    service.execute(user_id, hashed_password)

    return APIResponse.success_response(
        message="Password reset successfully"
    )



@router.post("/verify-email", response_model=APIResponse[None])
def verify_email(
    payload: schemas.EmailVerificationRequest,
    db: Session = Depends(get_db)
):

    user_id = verify_email_token(payload.token)

    if not user_id:
        return APIResponse.error_response("Invalid or expired token")

    repo = SQLAlchemyUserRepository(db)
    service = VerifyUserService(repo)
    service.execute(user_id)
    
    return APIResponse.success_response(
        message="Email verified successfully"
    )