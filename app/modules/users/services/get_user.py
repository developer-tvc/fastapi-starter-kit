from app.modules.users.entities.entities import User

class GetUser:
    def __init__(self, repo):
        self.repository = repo
    
    def execute(self, user_id: int) -> User:
        return self.repository.get_by_id(user_id)
