from abc import ABC, abstractmethod
from typing import List
from app.modules.users.entities.entities import User
from datetime import datetime

""" Abstract repository that defines the contract for user data operations
 This ensures the domain layer does not depend on database implementations
"""


class UserRepository(ABC):
    """method to retrieve all users
    Concrete implementations (e.g., SQLAlchemy) must implement this method
    """

    @abstractmethod
    def list_users(self) -> List[User]:
        pass

    """ method to create a new user
    Accepts a User domain entity and returns the created User
    """

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    """ method to get user by email
    Accepts an email and returns the User
    """

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass

    """ method to get user by id
    Accepts an id and returns the User
    """

    @abstractmethod
    def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def verify_user(self, user_id: int) -> User:
        pass

    @abstractmethod
    def update(self, user_id: int, user: dict) -> User:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass

    @abstractmethod
    def update_last_login(self, user_id: int, last_login_at: datetime) -> None:
        pass

    @abstractmethod
    def update_ip_address(self, user_id: int, ip_address: str) -> None:
        pass

    @abstractmethod
    def update_failed_login(
        self, user_id: int, is_locked: bool, locked_until: datetime
    ) -> None:
        pass

    @abstractmethod
    def update_failed_login_attempts(
        self, user_id: int, failed_login_attempts: int, attempt: bool
    ) -> None:
        pass
