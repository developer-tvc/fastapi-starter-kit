from sqlalchemy.orm import Session
from app.modules.users.domain.repositories import UserRepository
from app.modules.users.domain.entities import User
from app.modules.users.infrastructure.models import UserModel

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
    def create_user(self, email: str, password: str, full_name: str):
        
        new_user = UserModel(email=email, full_name=full_name, password=password, is_active=True)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return User(
            id=new_user.id,
            email=new_user.email,
            full_name=new_user.full_name,
            password_hash=new_user.password,
            is_active=new_user.is_active
        )