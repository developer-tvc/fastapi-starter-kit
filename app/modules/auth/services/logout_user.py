from jose import jwt
from fastapi import HTTPException
from app.core.security import SECRET_KEY, ALGORITHM
from app.modules.auth.adapters.blacklist_repository import BlacklistRepository


class LogoutUserService:

    def __init__(self, blacklist_repo: BlacklistRepository):
        self.blacklist_repo = blacklist_repo

    async def execute(self, token: str):

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        jti = payload.get("jti")

        if not jti:
            raise HTTPException(status_code=400, detail="Invalid token")

        self.blacklist_repo.add(jti)

        return {"message": "Successfully logged out"}
