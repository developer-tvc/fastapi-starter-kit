# Use case for listing all users
class ListUsers:
    # Initialize the use case with a user repository
    def __init__(self, repo):
        self.repo = repo

    # Execute the use case
    def execute(self):
        # Call the repository to fetch all users
        return self.repo.list_users()
