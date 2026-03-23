from app.core.exceptions import UserNotFound


class DeleteUser:
    def __init__(self, repo):
        self.repo = repo

    async def execute(self, user_id: int):
        existing_user = await self.repo.get_by_id(user_id)
        if not existing_user:
            raise UserNotFound(f"User with id {user_id} does not exist")
        return await self.repo.delete(user_id)