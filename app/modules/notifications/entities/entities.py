class Notification:
    def __init__(self, id: int, user_id: int, title: str, message: str):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.message = message