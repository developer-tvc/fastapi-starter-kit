from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from app.modules.users.entities.entities import User

""" Abstract repository that defines the contract for user data operations
 This ensures the domain layer does not depend on database implementations
"""


class UserRepository(ABC):
    """method to retrieve all users
    Concrete implementations (e.g., SQLAlchemy) must implement this method
    """

    @abstractmethod
    async def list_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        pass

    """ method to create a new user
    Accepts a User domain entity and returns the created User
    """

    @abstractmethod
    async def create_user(
        self,
        email: str,
        password: str,
        full_name: str,
        roles: list[int] = [],
        is_verified: bool = False,
    ) -> User:
        pass

    """ method to get user by email
    Accepts an email and returns the User
    """

    @abstractmethod
    async def get_by_email(self, email: str) -> User:
        pass

    """ method to get user by id
    Accepts an id and returns the User
    """

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    async def verify_user(self, user_id: int) -> User:
        pass

    @abstractmethod
    async def update(self, user_id: int, user: dict) -> User:
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def update_last_login(self, user_id: int, last_login_at: datetime) -> None:
        pass

    @abstractmethod
    async def update_ip_address(self, user_id: int, ip_address: str) -> None:
        pass

    @abstractmethod
    async def update_failed_login(
        self, user_id: int, is_locked: bool, locked_until: datetime
    ) -> None:
        pass

    @abstractmethod
    async def update_failed_login_attempts(
        self, user_id: int, failed_login_attempts: int, attempt: bool
    ) -> None:
        pass
