from app.modules.roles.entities.repositories import RoleRepository


class UpdateRole:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    def execute(self, role_id: int, name: str, description: str | None = None):
        return self.repo.update_role(role_id, name, description)
