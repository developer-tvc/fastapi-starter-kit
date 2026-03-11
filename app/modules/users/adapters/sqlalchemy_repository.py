from sqlalchemy.orm import Session
from app.modules.users.entities.repositories import UserRepository
from app.modules.users.entities.entities import User
from app.modules.users.adapters.models import UserModel
from app.modules.roles.adapters.models import UserRoleModel

""" Implementation of UserRepository using SQLAlchemy
 Concrete implementation of the UserRepository interface
"""
# Implementation of UserRepository using SQLAlchemy
class  SQLAlchemyUserRepository(UserRepository):
    # Initialize repository with database session
    def __init__(self, db: Session):
        self.db = db
    # Fetch all users from database
    def list_users(self):
        # Query all users from the users table
        users = self.db.query(UserModel).all()
        
        return [User(id=user.id, email=user.email, full_name=user.full_name, password_hash=user.password, is_active=user.is_active) for user in users]
    # Create a new user in the database
    def create_user(self, email: str, password: str, full_name: str, roles: list[int] = []):
        
        new_user = UserModel(email=email, full_name=full_name, password=password, is_active=True)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        # Assign roles
        for role_id in roles:
            user_role = UserRoleModel(
                user_id=new_user.id,
                role_id=role_id
            )
            self.db.add(user_role)
        self.db.commit()
        self.db.refresh(new_user)

        return User(
            id=new_user.id,
            email=new_user.email,
            full_name=new_user.full_name,
            password_hash=new_user.password,
            is_active=new_user.is_active,
            roles=[role.role_id for role in new_user.roles]
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
            is_active=user.is_active
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
            is_active=user.is_active
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
            is_active=user.is_active
        )
    