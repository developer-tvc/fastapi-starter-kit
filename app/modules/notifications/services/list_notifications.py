class ListNotificationsService:
    def __init__(self, repo):
        self.repo = repo

    async def execute(self, user_id: int):
        return await self.repo.get_all(user_id)
