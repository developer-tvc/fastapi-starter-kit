import pytest

from app.modules.users.services.create_users import CreateUser
from tests.users.fake_notification_service import FakeNotificationService
from tests.users.fake_repository import FakeUserRepository


@pytest.mark.asyncio
async def test_create_user():
    """
    Test that a user can be successfully created.
    """

    repo = FakeUserRepository()

    notification_service = FakeNotificationService()
    use_case = CreateUser(repo, notification_service)

    user = await use_case.execute(
        email="test@example.com",
        password="password123",
        full_name="Test User",
        roles=[],
        background_tasks=None,
        current_user=None,
    )

    assert user.id == 1
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.is_active is True
