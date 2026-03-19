import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

SMTP_SERVER = settings.SMTP_SERVER
SMTP_PORT = settings.SMTP_PORT
SMTP_USERNAME = settings.SMTP_USERNAME
SMTP_PASSWORD = settings.SMTP_PASSWORD


async def send_email(to_email: str, subject: str, body: str):
    
    if not settings.EMAIL_SERVICE:
        return

    # Decide recipients
    if settings.LIVE_MODE:
        recipients = [to_email]  # send to real user
    else:
        recipients = settings.TESTING_EMAIL  # redirect to testing emails

    msg = MIMEMultipart()
    msg["From"] = SMTP_USERNAME
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        for email in recipients:
            msg["To"] = email
            server.sendmail(SMTP_USERNAME, email, msg.as_string())
