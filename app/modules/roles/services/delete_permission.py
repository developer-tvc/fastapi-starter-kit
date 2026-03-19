from app.modules.roles.entities.repositories import RoleRepository


class DeletePermission:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    async def execute(self, permission_id: int):
        return await self.repo.delete_permissions(permission_id)
