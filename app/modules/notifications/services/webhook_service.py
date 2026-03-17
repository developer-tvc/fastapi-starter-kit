import requests
from app.core.config import settings


def send_webhook(payload: dict, repo):

    if not settings.WEBHOOK_NOTIFICATION_ENABLED:
        return

    for attempt in range(1, settings.MAX_WEBHOOK_RETRIES + 1):
        try:
            response = requests.post(settings.WEBHOOK_URL, json=payload, timeout=5)
            if response.status_code == 200:
                print(f"Webhook sent successfully")
                return

            print(f"Webhook sent successfully")

        except Exception as e:
            print(f"Failed to send webhook: {e}")

        if attempt < settings.MAX_WEBHOOK_RETRIES:
            time.sleep(settings.WEBHOOK_RETRY_DELAY)

    repo.create(
        user_id=payload["user_id"],
        title=payload["title"],
        message=payload["message"],
        channel="webhook",
        status="failed",
        error_message="Max retries reached",
    )
