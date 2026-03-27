from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notifications.adapters.models import (
    NotificationLogModel,
    NotificationModel,
)
from app.modules.notifications.entities.repositories import (
    NotificationLogRepository,
    NotificationRepository,
)


class NotificationRepository(NotificationRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int, title: str, message: str):

        notification = NotificationModel(user_id=user_id, title=title, message=message)
        print(notification, "---third")
        self.db.add(notification)
        await self.db.commit()

    async def get_all(self, user_id: int):
        result = await self.db.execute(select(NotificationModel))
        return result.scalars().all()


class NotificationLogRepository(NotificationLogRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        user_id: int,
        title: str,
        message: str,
        channel: str,
        status: str,
        error_message: str,
    ):
        notification_log = NotificationLogModel(
            user_id=user_id,
            title=title,
            message=message,
            channel=channel,
            status=status,
            error_message=error_message,
        )
        self.db.add(notification_log)
        await self.db.commit()
