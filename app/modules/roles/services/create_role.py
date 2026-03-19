from app.modules.roles.entities.repositories import RoleRepository


class CreateRole:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    async def execute(self, name: str, description: str | None = None):
        return await self.repo.create_role(name, description)
