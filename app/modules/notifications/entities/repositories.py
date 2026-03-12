from abc import ABC, abstractmethod
from typing import List
from app.modules.notifications.entities.entities import Notification

class NotificationRepository(ABC):
    @abstractmethod
    def get_all(self, user_id: int) -> List[Notification]:
        pass
 
    