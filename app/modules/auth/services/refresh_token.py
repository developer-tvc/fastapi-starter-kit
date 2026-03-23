from fastapi import HTTPException
from jose import JWTError, jwt

from app.core.security import ALGORITHM, SECRET_KEY, create_access_token


class RefreshTokenService:

    async def execute(self, refresh_token: str):

        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

            if payload.get("type") != "refresh":
                raise HTTPException(status_code=401, detail="Invalid token")

            user_id = payload.get("sub")

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        access_token = create_access_token({"sub": str(user_id)})

        return {"access_token": access_token, "token_type": "bearer"}
