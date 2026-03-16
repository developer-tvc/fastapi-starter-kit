from app.core.security import hash_password
from app.core.config import get_settings
from app.modules.notifications.services.notification_service import NotificationService
from app.core.security import create_email_verification_token
from app.core.services.email_templates import email_verification_template
settings = get_settings()

# Use case class responsible for creating a new user
class CreateUser:
    # Initialize the use case with a user repository
    def __init__(self, repo,notification_service):
        self.repo = repo
        self.notification_service=notification_service
    # Execute the user creation process
    def execute(self, email: str, password: str, full_name: str, roles: list[int] = [], background_tasks = None, current_user = None):
        
        # Hash the plain password before storing it in the database
        password_hash = hash_password(password)
        # verification flag
        is_verified = not settings.EMAIL_VERIFICATION_ENABLED
        # Call the repository to create and store the new user
        user = self.repo.create_user(email, password_hash, full_name, roles, is_verified)

        #Notification Service
        # send verification email
        if settings.EMAIL_VERIFICATION_ENABLED and background_tasks:
            token = create_email_verification_token(user.id)

            verify_link = f"{settings.EMAIL_VERIFICATION_LINK}?token={token}"

            body = email_verification_template(verify_link,full_name,settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            self.notification_service.send_email_notification(email, "Verify your email", body,background_tasks)
        
        creator = current_user.full_name if current_user else "System"
        self.notification_service.send_inapp_notification(
            user.id,
            "Account Created",
            f"Your account was created successfully by {creator}",
        )
        
        return user