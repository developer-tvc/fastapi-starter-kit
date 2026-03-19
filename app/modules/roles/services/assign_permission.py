from app.modules.roles.entities.repositories import RoleRepository


class AssignPermission:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    async def execute(self, role_id: int, permission_id: int):
        return await self.repo.assign_permission(role_id, permission_id)
