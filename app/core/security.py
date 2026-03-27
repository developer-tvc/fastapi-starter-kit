# Standard library
import uuid
from datetime import datetime, timedelta

# Third-party
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

# First-party (your app)
from app.core.config import settings
from app.core.dependencies import get_db
from app.modules.auth.adapters.blacklist_repository import BlacklistRepository
from app.modules.roles.adapters.sqlalchemy_repository import SQLAlchemyRoleRepository
from app.modules.roles.services.check_permission import CheckPermissionService
from app.modules.users.adapters.sqlalchemy_repository import SQLAlchemyUserRepository

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.SWAGGER_LOGIN)


limiter = Limiter(key_func=get_remote_address)


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

    to_encode.update({"exp": expire, "type": "access", "jti": str(uuid.uuid4())})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    """Create a JWT refresh token."""

    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()

    to_encode.update({"exp": expire, "type": "refresh", "jti": str(uuid.uuid4())})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    """Get current user from JWT token."""
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

        if await blacklist_repo.exists(jti):
            raise credentials_exception

        if user_id is None:
            raise credentials_exception

    except JWTError as exc:
        raise credentials_exception from exc

    repo = SQLAlchemyUserRepository(db)
    user = await repo.get_by_id(int(user_id))

    if user is None:
        raise credentials_exception

    # -----------------------------
    # Store user in request context
    # -----------------------------
    db.info["current_user"] = user

    return user


def verify_refresh_token(refresh_token: str):
    """Verify refresh token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
    )

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise credentials_exception

        return int(payload["sub"])

    except JWTError as exc:
        raise credentials_exception from exc


def require_permission(permission: str):
    """Require permission for a specific action."""

    async def permission_checker(
        current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
    ):

        repo = SQLAlchemyRoleRepository(db)
        service = CheckPermissionService(repo)

        allowed = await service.execute(current_user.id, permission)

        if not allowed:
            raise HTTPException(status_code=403, detail="Permission denied")
        return current_user

    return permission_checker


def create_password_reset_token(user_id: int):
    """Create password reset token."""
    expire = datetime.utcnow() + timedelta(minutes=30)

    payload = {"sub": str(user_id), "type": "password_reset", "exp": expire}

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_password_reset_token(token: str):
    """Verify password reset token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        if payload.get("type") != "password_reset":
            return None

        return int(payload.get("sub"))

    except JWTError:
        return None


def create_email_verification_token(user_id: int):
    """Create email verification token."""
    payload = {
        "sub": str(user_id),
        "type": "email_verification",
        "exp": datetime.utcnow() + timedelta(hours=24),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_email_token(token: str):
    """Verify email verification token."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        if payload.get("type") != "email_verification":
            return None

        return int(payload.get("sub"))

    except JWTError:
        return None
