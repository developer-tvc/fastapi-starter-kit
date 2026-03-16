
from app.modules.roles.entities.repositories import RoleRepository

class CreateRole:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    def execute(self, name: str, description: str | None = None):
        return self.repo.create_role(name, description)