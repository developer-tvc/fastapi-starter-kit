
from app.modules.users.entities.repositories import UserRepository

class VerifyUserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_id: int):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise Exception("User not found")
        return self.user_repository.verify_user(user_id)
