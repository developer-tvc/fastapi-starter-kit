from app.modules.roles.adapters.sqlalchemy_repository import \
    SQLAlchemyRoleRepository


class CheckPermissionService:

    def __init__(self, repo: SQLAlchemyRoleRepository):
        self.repo = repo

    def execute(self, user_id: int, permission: str):

        permissions = self.repo.get_user_permissions(user_id)
        if permission not in permissions:
            return False

        return True
