from app.modules.users.entities.repositories import UserRepository
from app.core.security import create_access_token, create_refresh_token, verify_password
from fastapi import HTTPException

class LoginUserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, email: str, password: str):
        user = self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid password")
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        return {"access_token": access_token, "refresh_token": refresh_token}