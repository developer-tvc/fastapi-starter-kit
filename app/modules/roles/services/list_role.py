from app.modules.roles.entities.repositories import RoleRepository

class ListRoles:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    def execute(self):
        return self.repo.list_roles()