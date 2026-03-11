from app.core.security import hash_password

# Use case class responsible for creating a new user
class CreateUser:
    # Initialize the use case with a user repository
    def __init__(self, repo):
        self.repo = repo
    # Execute the user creation process
    def execute(self, email: str, password: str, full_name: str, roles: list[int] = []):
        
        # Hash the plain password before storing it in the database
        password_hash = hash_password(password)
        # Call the repository to create and store the new user
        return self.repo.create_user(email, password_hash, full_name, roles)