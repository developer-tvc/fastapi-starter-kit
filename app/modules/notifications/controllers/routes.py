from fastapi import APIRouter, Depends
from app.core.dependencies import get_db
from app.core.security import require_permission
from app.modules.notifications import constants
from app.core.schemas.response import APIResponse
from app.modules.notifications.repositories.notification_repository import NotificationRepository
from app.modules.notifications.services.list_notifications import ListNotifications
from app.modules.notifications.controllers import schemas
from app.modules.users.entities.entities import User
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Notifications"],
)

@router.get("/", response_model=APIResponse[list[schemas.NotificationList]])
def read_notifications(db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(constants.VIEW_PERMISSION))
):
    repo = NotificationRepository(db)
    use_case = ListNotifications(repo)
    return APIResponse.success_response(
        data=use_case.execute(current_user.id),
        message="Notifications fetched successfully",
    )