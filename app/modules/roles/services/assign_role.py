from app.modules.roles.entities.repositories import RoleRepository


class AssignRole:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    async def execute(self, user_id: int, role_id: int):
        return await self.repo.assign_role(user_id, role_id)
