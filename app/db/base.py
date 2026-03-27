# app/db/base.py
from app.db.base_class import Base  # the actual declarative base
from app.modules.activity_logs.adapters.models import ActivityLogModel
from app.modules.auth.adapters.models import BlacklistedToken, UserDevice
from app.modules.notifications.adapters.models import (NotificationLogModel,
                                                       NotificationModel)
from app.modules.roles.adapters.models import (PermissionModel, RoleModel,
                                               RolePermissionModel,
                                               UserRoleModel)
# Import all models here so that Alembic sees them
from app.modules.users.adapters.models import UserModel
