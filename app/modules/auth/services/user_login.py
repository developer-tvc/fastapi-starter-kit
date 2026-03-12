from app.modules.users.entities.repositories import UserRepository
from app.core.security import create_access_token, create_refresh_token, verify_password
from fastapi import HTTPException
from datetime import datetime, timedelta
from app.modules.activity_logs.request_context import current_ip
from app.core.config import settings

class LoginUserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.db = user_repository.db

    async def execute(self, email: str, password: str):
        user = self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.is_verified:
            raise HTTPException(status_code=401, detail="User not verified. Please verify your email first.")
        #Check if login lock is enabled
        now = datetime.utcnow()
        if settings.LOGIN_LOCK_ENABLED:
            # If account is locked and still within lock window
            if user.is_locked and user.locked_until and user.locked_until > now:

                remaining_seconds = int((user.locked_until - now).total_seconds())
                remaining_minutes = remaining_seconds // 60
                remaining_seconds = remaining_seconds % 60

                raise HTTPException(
                    status_code=403,
                    detail=f"Account locked. Try again in {remaining_minutes}m {remaining_seconds}s"
                )

            # If lock time expired → reset lock
            if user.is_locked and user.locked_until and user.locked_until <= now:
                user.is_locked = False
                user.failed_login_attempts = 0
                user.locked_until = None

                self.user_repository.update_failed_login(user.id, False, None)
                self.user_repository.update_failed_login_attempts(user.id, 0, True)
        
        if not verify_password(password, user.password_hash):
            if settings.LOGIN_LOCK_ENABLED:
                user.failed_login_attempts += 1
                attempt = False
                if user.failed_login_attempts >= settings.LOGIN_MAX_ATTEMPTS:
                    user.is_locked = True
                    user.locked_until = datetime.utcnow() + timedelta(minutes=settings.LOGIN_LOCK_MINUTES)

                self.user_repository.update_failed_login(user.id, user.is_locked, user.locked_until)
                self.user_repository.update_failed_login_attempts(user.id, user.failed_login_attempts,attempt)
            raise HTTPException(status_code=401, detail="Invalid password")
        if settings.LOGIN_LOCK_ENABLED:
            user.failed_login_attempts = 0
            user.is_locked = False
            user.locked_until = None
            attempt = True
            self.user_repository.update_failed_login_attempts(user.id, user.failed_login_attempts,attempt)
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        user.last_login_at = datetime.utcnow()
        user.ip_address = current_ip.get()
        self.user_repository.update_last_login(user.id, user.last_login_at)
        self.user_repository.update_ip_address(user.id, user.ip_address)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }