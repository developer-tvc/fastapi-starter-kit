from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.core.schemas.response import APIResponse
from app.core.security import require_permission
from app.modules.notifications import constants
from app.modules.notifications.controllers import schemas
from app.modules.notifications.repositories.notification_repository import \
    NotificationRepository
from app.modules.notifications.services.list_notifications import \
    ListNotificationsService
from app.modules.users.entities.entities import User

router = APIRouter(
    tags=["Notifications"],
)


@router.get("/", response_model=APIResponse[list[schemas.NotificationList]])
async def read_notifications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission(constants.VIEW_PERMISSION)),
):
    repo = NotificationRepository(db)
    use_case = ListNotifications(repo)
    return APIResponse.success_response(
        data=await use_case.execute(current_user.id),
        message="Notifications fetched successfully",
    )
