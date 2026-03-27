from app.modules.roles.entities.repositories import RoleRepository


class DeleteRole:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    async def execute(self, role_id: int):
        return await self.repo.delete_role(role_id)
