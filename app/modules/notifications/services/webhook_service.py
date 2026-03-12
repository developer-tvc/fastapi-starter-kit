import requests
from app.core.config import settings


def send_webhook(payload: dict):

    if not settings.WEBHOOK_NOTIFICATION_ENABLED:
        return

    try:
        response = requests.post(
            settings.WEBHOOK_URL,
            json=payload,
            timeout=5
        )
        response.raise_for_status()
        print(f"Webhook sent successfully")

    except Exception as e:
        print(f"Failed to send webhook: {e}")