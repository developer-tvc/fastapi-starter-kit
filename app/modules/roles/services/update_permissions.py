from app.modules.roles.entities.repositories import RoleRepository

class UpdatePermissions:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    def execute(self, permission_id: int, name: str):
        return self.repo.update_permissions(permission_id, name)