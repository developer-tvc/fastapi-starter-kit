from app.modules.roles.entities.repositories import RoleRepository


class GetUserPermissions:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    def execute(self, user_id: int):
        return self.repo.get_user_permissions(user_id)
