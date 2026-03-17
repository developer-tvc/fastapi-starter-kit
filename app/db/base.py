"""
Base file for importing all database models.
"""

# pylint: disable=wildcard-import, unused-wildcard-import
from app.modules.users.adapters.models import *
from app.modules.auth.adapters.models import *
from app.modules.roles.adapters.models import *
from app.modules.activity_logs.adapters.models import *
from app.modules.notifications.adapters.models import *
