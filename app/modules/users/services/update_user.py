from app.core.exceptions import UserNotFound


class UpdateUser:
    def __init__(self, repo):
        self.repo = repo

    async def execute(self, user_id: int, user: dict):
        # Check if user exists first
        existing_user = await self.repo.get_by_id(user_id)
        if not existing_user:
            raise UserNotFound(f"User with id {user_id} does not exist")
        user_data = user.model_dump(exclude_unset=True)
        return await self.repo.update(user_id, user_data)
