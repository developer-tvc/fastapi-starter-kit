from app.modules.roles.entities.repositories import RoleRepository

class UnassignPermission:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    def execute(self, role_id: int, permission_id: int):
        return self.repo.unassign_permission(role_id, permission_id)
