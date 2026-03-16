class DeleteUser:
    def __init__(self, repo):
        self.repo = repo
    
    def execute(self, user_id: int):
        return self.repo.delete(user_id)
