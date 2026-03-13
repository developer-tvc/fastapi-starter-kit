from app.core.config import settings
from app.core.services.email_service import send_email
from app.modules.notifications.services.sms_service import send_sms
from app.modules.notifications.services.webhook_service import send_webhook

class NotificationService:

    def __init__(self, repo):
        self.repo = repo

    def send_email_notification(self, email, subject, message,background_tasks):  

        background_tasks.add_task(
            send_email,
            email,
            subject,
            message
        )

    def send_sms_notification(self, phone, message):

        if settings.SMS_NOTIFICATION_ENABLED:
            send_sms(phone, message)

    def send_inapp_notification(self, user_id, title, message):

        if settings.IN_APP_NOTIFICATION_ENABLED:
            self.repo.create(user_id, title, message)

    def send_webhook_notification(self, payload,background_tasks):

        if settings.WEBHOOK_NOTIFICATION_ENABLED:
            background_tasks.add_task(
                send_webhook,
                payload,
                self.repo
            )