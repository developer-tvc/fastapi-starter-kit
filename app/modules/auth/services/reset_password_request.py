from app.modules.users.adapters.sqlalchemy_repository import SQLAlchemyUserRepository
from app.core.security import create_password_reset_token
from app.core.services.email_templates import password_reset_email
from app.core.services.email_service import send_email

class ResetPasswordRequestService:
    def __init__(self, repo: SQLAlchemyUserRepository):
        self.repo = repo
    
    def execute(self, payload, background_tasks):
        user = self.repo.get_by_email(payload.email)

        if user:
            token = create_password_reset_token(user.id)

            reset_link = f"http://localhost:3000/reset-password?token={token}"

            subject = "Password Reset Request"

            body = password_reset_email(reset_link)

            background_tasks.add_task(
                send_email,
                user.email,
                subject,
                body
            )