from datetime import datetime

class Notification:
    def __init__(self, id: int, user_id: int, title: str, message: str):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.message = message


class NotificationLog:
    def __init__(self, id: int, user_id: int, title: str, message: str, channel: str, status: str, error_message: str, created_at: datetime):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.message = message
        self.channel = channel
        self.status = status
        self.error_message = error_message
        self.created_at = created_at