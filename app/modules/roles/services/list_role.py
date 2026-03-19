from app.modules.roles.entities.repositories import RoleRepository


class ListRoles:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    async def execute(self):
        return await self.repo.list_roles()
