from app.modules.notifications.adapters.models import NotificationModel
from app.modules.notifications.entities.repositories import NotificationRepository
from app.modules.notifications.adapters.models import NotificationLogModel
from app.modules.notifications.entities.repositories import NotificationLogRepository

class NotificationRepository(NotificationRepository):

    def __init__(self, db):
        self.db = db

    def create(self, user_id: int, title: str, message: str):

        notification = NotificationModel(
            user_id=user_id,
            title=title,
            message=message
        )

        self.db.add(notification)
        self.db.commit()
    
    def get_all(self, user_id: int):
        return self.db.query(NotificationModel).all()



class NotificationLogRepository(NotificationLogRepository):

    def __init__(self, db):
        self.db = db

    def create(self, user_id: int, title: str, message: str, channel: str, status: str, error_message: str):
        notification_log = NotificationLogModel(
            user_id=user_id,
            title=title,
            message=message,
            channel=channel,
            status=status,
            error_message=error_message
        )
        self.db.add(notification_log)
        self.db.commit()