from typing import List, Optional


class Permission:
    """
    Domain entity representing a permission.

    Permissions define actions that can be performed in the system.

    Examples:
        user:view
        user:create
        user:update
        user:delete
    """

    def __init__(
        self,
        id: int,
        name: str,
    ):
        self.id = id
        self.name = name


class Role:
    """
    Domain entity representing a role.

    Roles group multiple permissions together.

    Examples:
        Admin
        Manager
        User
    """

    def __init__(
        self,
        id: int,
        name: str,
        description: Optional[str] = None,
        permissions: Optional[List[Permission]] = None,
    ):
        self.id = id
        self.name = name
        self.description = description

        # Role can have multiple permissions
        self.permissions = permissions or []


class RolePermission:
    """
    Domain representation of the Role-Permission relationship.

    Maps roles to permissions.
    """

    def __init__(
        self,
        role_id: int,
        permission_id: int,
    ):
        self.role_id = role_id
        self.permission_id = permission_id


class UserRole:
    """
    Domain representation of the User-Role relationship.

    A user can have multiple roles.
    """

    def __init__(
        self,
        user_id: int,
        role_id: int,
    ):
        self.user_id = user_id
        self.role_id = role_id