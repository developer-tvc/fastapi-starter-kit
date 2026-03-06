from typing import List

from app.modules.users.domain.entities import User
from app.modules.users.domain.repositories import UserRepository


class FakeUserRepository(UserRepository):
    """
    In-memory fake implementation of UserRepository for tests.

    Follows the same contract as the domain repository interface so that
    use cases and services can be tested without a real database.
    """

    def __init__(self):
        self.users = []

    def list_users(self):
        """Return all users stored in memory."""
        return self.users

    def create_user(self, email: str, password: str, full_name: str):
        """Create a new user and store it in memory."""

        user = User(
            id=len(self.users) + 1,
            email=email,
            full_name=full_name,
            password_hash=password,
            is_active=True
        )

        self.users.append(user)
        return user
