from app.core.config import settings
from app.modules.notifications.constants import MOCK, TWILIO


def send_sms(phone: str, message: str):

    if not settings.SMS_NOTIFICATION_ENABLED:
        return

    if settings.SMS_PROVIDER == MOCK:
        print(f"[SMS MOCK] {phone} -> {message}")

    elif settings.SMS_PROVIDER == TWILIO:
        # integrate later
        pass

    else:
        raise ValueError("Unsupported SMS provider")
