from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.modules.users.adapters.sqlalchemy_repository import SQLAlchemyUserRepository
from jose import JWTError
from fastapi.security import HTTPAuthorizationCredentials
import uuid
from app.modules.auth.adapters.blacklist_repository import BlacklistRepository
from app.modules.roles.adapters.sqlalchemy_repository import SQLAlchemyRoleRepository
from app.modules.roles.services.check_permission import CheckPermissionService

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.SWAGGER_LOGIN)


def hash_password(password: str) -> str:
    """Return a secure hash for the given plaintext password."""
    return pwd_context.hash(password)



def verify_password(plain, hashed):
    """Verify that a given plaintext password matches a hashed password."""
    return pwd_context.verify(plain, hashed)



def create_access_token(data: dict):
    """Create a JWT access token."""
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()

    to_encode.update({
        "exp": expire,
        "type": "access",
        "jti": str(uuid.uuid4())
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    """Create a JWT refresh token."""

    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()

    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "jti": str(uuid.uuid4())
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "access":
            raise credentials_exception

        user_id = payload.get("sub")
        jti = payload.get("jti")

        blacklist_repo = BlacklistRepository(db)

        if blacklist_repo.exists(jti):
            raise credentials_exception

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    repo = SQLAlchemyUserRepository(db)
    user = repo.get_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user


def verify_refresh_token(refresh_token: str):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token"
    )

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise credentials_exception

        return payload["sub"]

    except JWTError:
        raise credentials_exception



def require_permission(permission: str):

    def permission_checker(
        current_user = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):

        repo = SQLAlchemyRoleRepository(db)
        service = CheckPermissionService(repo)

        allowed = service.execute(current_user.id, permission)

        if not allowed:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
        return current_user

    return permission_checker