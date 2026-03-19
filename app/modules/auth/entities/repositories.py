from abc import ABC, abstractmethod
from app.modules.auth.entities.entities import UserDeviceEntity


class DeviceRegisterRepository(ABC):
    @abstractmethod
    async def create(
        self,
        user_id: int,
        device_id: str,
        device_name: str,
        user_agent: str,
        ip_address: str,
    ) -> UserDeviceEntity:
        pass
