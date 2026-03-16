from abc import ABC, abstractmethod
from typing import List

from app.modules.notifications.entities.entities import Notification


class NotificationRepository(ABC):
    @abstractmethod
    def get_all(self, user_id: int) -> List[Notification]:
        pass

    @abstractmethod
    def create(self, user_id: int, title: str, message: str):
        pass


class NotificationLogRepository(ABC):
    @abstractmethod
    def create(
        self,
        user_id: int,
        title: str,
        message: str,
        channel: str,
        status: str,
        error_message: str,
    ):
        pass
