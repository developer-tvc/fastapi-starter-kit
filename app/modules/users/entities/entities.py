from datetime import datetime

class User:

    """
    Domain Entity representing a system user.

    This class contains the core business rules related to a user.
    It is independent of frameworks, databases, or APIs.

    Notes:
        - This entity intentionally stores only a password hash (never a raw password).
        - Input validation/normalization (e.g., email format, trimming) is typically enforced
          at the boundaries (use-cases / services) before constructing the entity.
    """

    def __init__(self, id: int, email: str, full_name: str, password_hash: str, is_active: bool = True, roles: list[int] = [], is_verified: bool = False, last_login_at: datetime = None, ip_address: str = None, failed_login_attempts: int = 0, is_locked: bool = False, locked_until: datetime = None):
        """
        Create a new User entity.

        Args:
            id (int): Unique identifier for the user.
            email (str): User email address.
            full_name (str): Display name used in the domain (not an auth credential).
            password_hash (str): Hashed password for authentication.
            is_active (bool): Indicates if the user account is active.
        """
        # Domain invariants are kept simple here; persistence concerns (DB IDs) remain external.
        self.id = id
        self.email = email
        self.full_name = full_name
        self.password_hash = password_hash  # hash only; never store or accept plaintext here
        self.is_active = is_active
        self.roles = roles
        self.is_verified = is_verified
        self.last_login_at = last_login_at
        self.ip_address = ip_address
        self.failed_login_attempts = failed_login_attempts
        self.is_locked = is_locked
        self.locked_until = locked_until

    def deactivate(self):
        """
        Deactivate the user account.

        Business Rule:
        A deactivated user cannot log in to the system.
        """
        # Explicit state transition in the domain model.
        self.is_active = False

    def activate(self):
        """
        Activate the user account.

        Business Rule:
        Allows the user to log in again.
        """
        # Explicit state transition in the domain model.
        self.is_active = True
    