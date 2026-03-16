from app.modules.roles.entities.repositories import RoleRepository


class AssignRole:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    def execute(self, user_id: int, role_id: int):
        return self.repo.assign_role(user_id, role_id)
