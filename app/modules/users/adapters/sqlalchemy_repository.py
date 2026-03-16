from datetime import datetime

from sqlalchemy.orm import Session

from app.modules.roles.adapters.models import UserRoleModel
from app.modules.users.adapters.models import UserModel
from app.modules.users.entities.entities import User
from app.modules.users.entities.repositories import UserRepository

""" Implementation of UserRepository using SQLAlchemy
 Concrete implementation of the UserRepository interface
"""


# Implementation of UserRepository using SQLAlchemy
class SQLAlchemyUserRepository(UserRepository):
    # Initialize repository with database session
    def __init__(self, db: Session):
        self.db = db

    # Fetch all users from database
    def list_users(self):
        # Query all users from the users table
        users = self.db.query(UserModel).all()

        return [
            User(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                password_hash=user.password,
                is_active=user.is_active,
            )
            for user in users
        ]

    # Create a new user in the database
    def create_user(
        self,
        email: str,
        password: str,
        full_name: str,
        roles: list[int] = [],
        is_verified: bool = False,
    ):

        new_user = UserModel(
            email=email,
            full_name=full_name,
            password=password,
            is_active=True,
            is_verified=is_verified,
        )
        self.db.add(new_user)
        self.db.flush()

        # Assign roles
        for role_id in roles:
            user_role = UserRoleModel(user_id=new_user.id, role_id=role_id)
            self.db.add(user_role)
        self.db.commit()
        self.db.refresh(new_user)

        return User(
            id=new_user.id,
            email=new_user.email,
            full_name=new_user.full_name,
            password_hash=new_user.password,
            is_active=new_user.is_active,
            roles=[role.role_id for role in new_user.roles],
            is_verified=new_user.is_verified,
        )

    def get_by_email(self, email: str):
        user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            return None
        return User(
            id=user.id,
            email=user.email,
            password_hash=user.password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            failed_login_attempts=user.failed_login_attempts,
            is_locked=user.is_locked,
            locked_until=user.locked_until,
        )

    def get_by_id(self, user_id: int):
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        return User(
            id=user.id,
            email=user.email,
            password_hash=user.password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
        )

    def update_password(self, user_id: int, password: str):
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        user.password = password
        self.db.commit()
        self.db.refresh(user)
        return User(
            id=user.id,
            email=user.email,
            password_hash=user.password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
        )

    def verify_user(self, user_id: int):
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        user.is_verified = True
        self.db.commit()
        self.db.refresh(user)
        return User(
            id=user.id,
            email=user.email,
            password_hash=user.password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
        )

    def get_by_id(self, user_id: int):
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        return User(
            id=user.id,
            email=user.email,
            password_hash=user.password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
        )

    def update(self, user_id: int, user: dict):

        user_obj = self.db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user_obj:
            return None

        # extract roles
        roles = user.pop("roles", None)

        # update normal fields
        for key, value in user.items():
            setattr(user_obj, key, value)

        # update roles
        if roles is not None:

            # remove existing roles
            self.db.query(UserRoleModel).filter(
                UserRoleModel.user_id == user_id
            ).delete()

            # insert new roles
            for role_id in roles:
                self.db.add(UserRoleModel(user_id=user_id, role_id=role_id))

        self.db.commit()
        self.db.refresh(user_obj)

        return User(
            id=user_obj.id,
            email=user_obj.email,
            password_hash=user_obj.password,
            full_name=user_obj.full_name,
            is_active=user_obj.is_active,
            is_verified=user_obj.is_verified,
            roles=roles if roles else [r.role_id for r in user_obj.roles],
        )

    def delete(self, user_id: int) -> None:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        user.is_deleted = True
        user.deleted_at = datetime.utcnow()

        self.db.commit()

    def update_last_login(self, user_id: int, last_login_at: datetime) -> None:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        user.last_login_at = last_login_at
        self.db.commit()
        self.db.refresh(user)
        return User(
            id=user.id,
            email=user.email,
            password_hash=user.password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            last_login_at=user.last_login_at,
        )

    def update_ip_address(self, user_id: int, ip_address: str) -> None:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        user.ip_address = ip_address
        self.db.commit()
        self.db.refresh(user)
        return User(
            id=user.id,
            email=user.email,
            password_hash=user.password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            ip_address=user.ip_address,
        )

    def update_failed_login(
        self, user_id: int, is_locked: bool, locked_until: datetime
    ) -> None:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            return None

        user.is_locked = is_locked
        user.locked_until = locked_until

        self.db.commit()
        self.db.refresh(user)
        return User(
            id=user.id,
            email=user.email,
            password_hash=user.password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            is_locked=user.is_locked,
            locked_until=user.locked_until,
        )

    def update_failed_login_attempts(
        self, user_id: int, failed_login_attempts: int, attempt: bool
    ) -> None:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        if not attempt:
            user.failed_login_attempts += 1
        else:
            user.failed_login_attempts = 0

        self.db.commit()
        self.db.refresh(user)
        return User(
            id=user.id,
            email=user.email,
            password_hash=user.password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            failed_login_attempts=user.failed_login_attempts,
        )
