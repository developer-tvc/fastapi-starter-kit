from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.adapters.models import BlacklistedToken


class BlacklistRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, jti: str):
        token = BlacklistedToken(jti=jti)
        self.db.add(token)
        await self.db.commit()

    async def exists(self, jti: str):
        result = await self.db.execute(select(BlacklistedToken).filter(BlacklistedToken.jti == jti))
        return result.scalar_one_or_none() is not None
