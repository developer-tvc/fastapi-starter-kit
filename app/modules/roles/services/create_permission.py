class CreatePermission:

    def __init__(self, repo):
        self.repo = repo

    def execute(self, name: str):
        return self.repo.create_permission(name)