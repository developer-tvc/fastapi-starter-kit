from app.modules.users.use_cases.create_users import CreateUser
from tests.users.fake_repository import FakeUserRepository


def test_create_user():
    """
    Test that a user can be successfully created.
    """

    repo = FakeUserRepository()
    use_case = CreateUser(repo)

    user = use_case.execute(
        email="test@example.com",
        password="password123",
        full_name="Test User"
    )

    assert user.id == 1
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.is_active is True