from app.modules.users.services.list_users import ListUsers
from tests.users.fake_repository import FakeUserRepository
import pytest

@pytest.mark.asyncio
async def test_list_users():
    """
    Test that users can be retrieved.
    """

    repo = FakeUserRepository()

    # Create fake users
    await repo.create_user("user1@test.com", "pass1", "User One")
    await repo.create_user("user2@test.com", "pass2", "User Two")

    use_case = ListUsers(repo)

    users = await use_case.execute()

    assert len(users) == 2
    assert users[0].email == "user1@test.com"
    assert users[1].email == "user2@test.com"
