class UpdateUser:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, user_id: int, user: dict):
        user_data = user.model_dump(exclude_unset=True)
        return self.repo.update(user_id, user_data)
