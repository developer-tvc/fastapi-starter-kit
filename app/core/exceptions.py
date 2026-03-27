class UserNotFound(Exception):
    """Raised when a user with the given ID does not exist."""

    pass


class EmailAlreadyExists(Exception):
    """Raised when trying to create a user with a duplicate email."""

    pass


class PermissionDenied(Exception):
    """Raised when a user lacks required permissions."""

    pass
