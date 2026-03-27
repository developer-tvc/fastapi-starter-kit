PERMISSIONS = [
    # User
    "user:create",
    "user:view",
    "user:update",
    "user:delete",
    # Permission
    "permission:create",
    "permission:view",
    "permission:update",
    "permission:delete",
    "permission:assign",
    "permission:unassign",
    # Role
    "role:create",
    "role:view",
    "role:update",
    "role:delete",
    "role:assign",
    "role:unassign",
    # User-Permission
    "user_permission:view",
    # Notification
    "notification:view",
]


ROLES = [
    {"name": "admin", "description": "System administrator"},
    {"name": "user", "description": "Regular user"},
]
