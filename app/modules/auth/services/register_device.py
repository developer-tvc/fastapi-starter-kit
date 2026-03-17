from app.modules.auth.entities.repositories import DeviceRegisterRepository
from app.modules.auth.entities.entities import UserDeviceEntity
from fastapi import Request
import uuid
from datetime import datetime


class RegisterDeviceService:
    def __init__(self, device_repository: DeviceRegisterRepository):
        self.device_repository = device_repository

    def execute(self, user_id: int, request) -> UserDeviceEntity:
        device_id = request.headers.get("X-Device-ID")

        if not device_id:
            device_id = str(uuid.uuid4())

        user_agent = request.headers.get("user-agent")
        ip_address = request.client.host
        # device name from client or fallback to user-agent
        device_name = request.headers.get("X-Device-Name")
        if device_name is None:
            device_name = user_agent
        device = self.device_repository.get_by_device_id(device_id)

        if device:
            device.last_used = datetime.utcnow()
            return device

        return self.device_repository.create(
            user_id=user_id,
            device_id=device_id,
            device_name=device_name,
            user_agent=user_agent,
            ip_address=ip_address,
        )
