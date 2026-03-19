from app.modules.users.entities.entities import User
from app.core.exceptions import UserNotFound


class GetUser:
    def __init__(self, repo):
        self.repository = repo

    def execute(self, user_id: int) -> User:
        existing_user = self.repository.get_by_id(user_id)
        if not existing_user:
            raise UserNotFound(f"User with id {user_id} does not exist")
        return self.repository.get_by_id(user_id)
