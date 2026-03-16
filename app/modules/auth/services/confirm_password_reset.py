from app.modules.users.adapters.sqlalchemy_repository import SQLAlchemyUserRepository

class ConfirmPasswordResetService:
    def __init__(self, user_repository: SQLAlchemyUserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id, hashed_password):
        self.user_repository.update_password(user_id, hashed_password)
        return True