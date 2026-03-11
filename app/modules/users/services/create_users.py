from app.core.security import hash_password
from app.core.config import get_settings
from app.core.services.email_service import send_email
from app.core.security import create_email_verification_token
from app.core.services.email_templates import email_verification_template

settings = get_settings()

# Use case class responsible for creating a new user
class CreateUser:
    # Initialize the use case with a user repository
    def __init__(self, repo):
        self.repo = repo
    # Execute the user creation process
    def execute(self, email: str, password: str, full_name: str, roles: list[int] = [], background_tasks = None):
        
        # Hash the plain password before storing it in the database
        password_hash = hash_password(password)
        # verification flag
        is_verified = not settings.EMAIL_VERIFICATION_ENABLED
        # Call the repository to create and store the new user
        user = self.repo.create_user(email, password_hash, full_name, roles, is_verified)
        # send verification email
        if settings.EMAIL_VERIFICATION_ENABLED and background_tasks:

            token = create_email_verification_token(user.id)

            verify_link = f"http://localhost:3000/verify-email?token={token}"

            body = email_verification_template(verify_link)

            background_tasks.add_task(
                send_email,
                user.email,
                "Verify your email",
                body
            )

        return user