# app/db/base.py
from app.db.base_class import Base  # the actual declarative base

# Import all models here so that Alembic sees them
from app.modules.users.adapters.models import UserModel
from app.modules.roles.adapters.models import RoleModel, PermissionModel, RolePermissionModel, UserRoleModel
from app.modules.activity_logs.adapters.models import ActivityLogModel
from app.modules.notifications.adapters.models import NotificationModel, NotificationLogModel
from app.modules.auth.adapters.models import UserDevice, BlacklistedToken