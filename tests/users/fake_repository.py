from datetime import datetime
from typing import List

from app.modules.notifications.entities.repositories import NotificationRepository
from app.modules.users.entities.entities import User
from app.modules.users.entities.repositories import UserRepository


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

    def create_user(
        self,
        email: str,
        password: str,
        full_name: str,
        roles: list[int] = [],
        is_verified: bool = False,
    ):
        """Create a new user and store it in memory."""

        user = User(
            id=len(self.users) + 1,
            email=email,
            full_name=full_name,
            password_hash=password,
            is_active=True,
            roles=roles or [],
            is_verified=is_verified,
        )

        self.users.append(user)
        return user

    def delete(self, user_id: int) -> None:
        """Delete a user by ID."""
        self.users = [user for user in self.users if user.id != user_id]
        return None

    def update(self, user_id: int, user: dict) -> User:
        """Update a user by ID."""
        for i, u in enumerate(self.users):
            if u.id == user_id:
                self.users[i] = User(**{**u.dict(), **user})
                return self.users[i]
        return None

    def get_by_email(self, email: str) -> User:
        """Get a user by email."""
        for user in self.users:
            if user.email == email:
                return user
        return None

    def get_by_id(self, user_id: int) -> User:
        """Get a user by ID."""
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def verify_user(self, user_id: int) -> User:
        """Verify a user by ID."""
        for user in self.users:
            if user.id == user_id:
                user.is_active = True
                return user
        return None

    def update_last_login(self, user_id: int, last_login_at: datetime) -> None:
        """Update the last login time for a user."""
        for user in self.users:
            if user.id == user_id:
                user.last_login_at = last_login_at
                return None
        return None

    def update_ip_address(self, user_id: int, ip_address: str) -> None:
        """Update the IP address for a user."""
        for user in self.users:
            if user.id == user_id:
                user.ip_address = ip_address
                return None
        return None

    def update_failed_login(
        self, user_id: int, is_locked: bool, locked_until: datetime
    ) -> None:
        """Update the failed login status for a user."""
        for user in self.users:
            if user.id == user_id:
                user.is_locked = is_locked
                user.locked_until = locked_until
                return None
        return None

    def update_failed_login_attempts(
        self, user_id: int, failed_login_attempts: int, attempt: bool
    ) -> None:
        """Update the failed login attempts for a user."""
        for user in self.users:
            if user.id == user_id:
                user.failed_login_attempts = failed_login_attempts
                user.attempt = attempt
                return None
        return None


class NotificationRepository(NotificationRepository):

    def __init__(self):
        self.users = []
        self.NotificationModel = None

    def create(self, user_id: int, title: str, message: str):

        notification = self.NotificationModel(
            user_id=user_id, title=title, message=message
        )

        self.users.append(notification)

    def get_all(self, user_id: int):
        return [user for user in self.users if user.user_id == user_id]
