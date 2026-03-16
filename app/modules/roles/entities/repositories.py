from abc import ABC, abstractmethod
from typing import List


class RoleRepository(ABC):

    @abstractmethod
    def get_user_permissions(self, user_id: int) -> List[str]:
        pass

    @abstractmethod
    def create_permission(self, name: str):
        pass

    @abstractmethod
    def list_permissions(self):
        pass

    @abstractmethod
    def update_permissions(self, permission_id: int, name: str):
        pass

    @abstractmethod
    def delete_permissions(self, permission_id: int):
        pass

    @abstractmethod
    def create_role(self, name: str, description: str | None = None):
        pass

    @abstractmethod
    def list_roles(self):
        pass

    @abstractmethod
    def update_role(self, role_id: int, name: str, description: str | None = None):
        pass

    @abstractmethod
    def delete_role(self, role_id: int):
        pass

    @abstractmethod
    def assign_permission(self, role_id: int, permission_id: int):
        pass

    @abstractmethod
    def unassign_permission(self, role_id: int, permission_id: int):
        pass

    @abstractmethod
    def get_user_permissions(self, user_id: int) -> List[str]:
        pass

    @abstractmethod
    def assign_role(self, user_id: int, role_id: int):
        pass

    @abstractmethod
    def unassign_role(self, user_id: int, role_id: int):
        pass
