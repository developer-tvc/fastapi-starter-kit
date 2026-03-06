from abc import ABC, abstractmethod
from typing import List
from app.modules.users.domain.entities import User

""" Abstract repository that defines the contract for user data operations
 This ensures the domain layer does not depend on database implementations
"""
class UserRepository(ABC):

    """ method to retrieve all users
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