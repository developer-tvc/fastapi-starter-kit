from fastapi import APIRouter, Depends
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
    print("token", token)
    blacklist_repo = BlacklistRepository(db)
    service = LogoutUserService(blacklist_repo)

    return await service.execute(token)