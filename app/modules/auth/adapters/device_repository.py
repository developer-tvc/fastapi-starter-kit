from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.adapters.models import UserDevice
from app.modules.auth.entities.entities import UserDeviceEntity
from app.modules.auth.entities.repositories import DeviceRegisterRepository


class DeviceRepository(DeviceRegisterRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_device_id(self, device_id):
        result = await self.db.execute(select(UserDevice).filter(UserDevice.device_id == device_id))
        return result.scalar_one_or_none()

    async def create(
        self,
        user_id: int,
        device_id: str,
        device_name: str,
        user_agent: str,
        ip_address: str,
    ) -> UserDeviceEntity:
        device = UserDevice(
            user_id=user_id,
            device_id=device_id,
            device_name=device_name,
            user_agent=user_agent,
            ip_address=ip_address,
        )
        self.db.add(device)
        await self.db.commit()
        await self.db.refresh(device)
        return device
