class CreatePermission:

    def __init__(self, repo):
        self.repo = repo

    async def execute(self, name: str):
        return await self.repo.create_permission(name)
