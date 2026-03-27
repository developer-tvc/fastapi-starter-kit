from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
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
    def __init__(self, db: AsyncSession):
        self.db = db

    # Fetch all users from database

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            full_name=model.full_name,
            password_hash=model.password,
            is_active=model.is_active,
            is_verified=model.is_verified,
        )
    
    async def list_users(self,skip:int = 0,limit:int = 10) -> list[User]:
        # Execute the select query asynchronously
        result = await self.db.execute(select(UserModel).offset(skip).limit(limit))
        users = result.scalars().all()  # this returns a list of UserModel
        # Get total count
        total_result = await self.db.execute(
            select(func.count()).select_from(UserModel)
        )
        total = total_result.scalar()


        # Map to domain entities
        return [self._to_entity(user) for user in users], total

    # Create a new user in the database
    async def create_user(
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
        await self.db.flush()

        # Assign roles
        for role_id in roles:
            user_role = UserRoleModel(user_id=new_user.id, role_id=role_id)
            self.db.add(user_role)
        await self.db.commit()
        await self.db.refresh(new_user)

        return User(
            id=new_user.id,
            email=new_user.email,
            full_name=new_user.full_name,
            password_hash=new_user.password,
            is_active=new_user.is_active,
            roles=roles,
            is_verified=new_user.is_verified,
        )

    async def get_by_email(self, email: str):
        user = await self.db.execute(select(UserModel).where(UserModel.email == email))
        user = user.scalar_one_or_none()
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

    async def get_by_id(self, user_id: int):
        user = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user = user.scalar_one_or_none()
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

    async def update_password(self, user_id: int, password: str):
        user = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user = user.scalar_one_or_none()
        if not user:
            return None
        user.password = password
        await self.db.commit()
        await self.db.refresh(user)
        return User(
            id=user.id,
            email=user.email,
            password_hash=user.password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
        )

    async def verify_user(self, user_id: int):
        user = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user = user.scalar_one_or_none()
        if not user:
            return None
        user.is_verified = True
        await self.db.commit()
        await self.db.refresh(user)
        return User(
            id=user.id,
            email=user.email,
            password_hash=user.password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
        )

    async def get_by_id(self, user_id: int):
        user = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user = user.scalar_one_or_none()
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

    async def update(self, user_id: int, user: dict):

        user_obj = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user_obj = user_obj.scalar_one_or_none()
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
            await self.db.execute(select(UserRoleModel).where(UserRoleModel.user_id == user_id))

            # insert new roles
            for role_id in roles:
                self.db.add(UserRoleModel(user_id=user_id, role_id=role_id))

        await self.db.commit()
        await self.db.refresh(user_obj)

        if roles is None:
            roles_result = await self.db.execute(select(UserRoleModel.role_id).where(UserRoleModel.user_id == user_id))
            roles = roles_result.scalars().all()

        return User(
            id=user_obj.id,
            email=user_obj.email,
            password_hash=user_obj.password,
            full_name=user_obj.full_name,
            is_active=user_obj.is_active,
            is_verified=user_obj.is_verified,
            roles=roles,
        )

    async def delete(self, user_id: int) -> None:
        user = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user = user.scalar_one_or_none()
        if not user:
            return None
        user.is_deleted = True
        user.deleted_at = datetime.utcnow()
        await self.db.commit()

    async def update_last_login(self, user_id: int, last_login_at: datetime) -> None:
        user = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user = user.scalar_one_or_none()
        if not user:
            return None
        user.last_login_at = last_login_at
        await self.db.commit()
        await self.db.refresh(user)
        return User(
            id=user.id,
            email=user.email,
            password_hash=user.password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            last_login_at=user.last_login_at,
        )

    async def update_ip_address(self, user_id: int, ip_address: str) -> None:
        user = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user = user.scalar_one_or_none()
        if not user:
            return None
        user.ip_address = ip_address
        await self.db.commit()
        await self.db.refresh(user)
        return User(
            id=user.id,
            email=user.email,
            password_hash=user.password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            ip_address=user.ip_address,
        )

    async def update_failed_login(
        self, user_id: int, is_locked: bool, locked_until: datetime
    ) -> None:
        user = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user = user.scalar_one_or_none()
        if not user:
            return None

        user.is_locked = is_locked
        user.locked_until = locked_until

        await self.db.commit()
        await self.db.refresh(user)
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

    async def update_failed_login_attempts(
        self, user_id: int, failed_login_attempts: int, attempt: bool
    ) -> None:
        user = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        user = user.scalar_one_or_none()
        if not user:
            return None
        if not attempt:
            user.failed_login_attempts += 1
        else:
            user.failed_login_attempts = 0

        await self.db.commit()
        await self.db.refresh(user)
        return User(
            id=user.id,
            email=user.email,
            password_hash=user.password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            failed_login_attempts=user.failed_login_attempts,
        )
