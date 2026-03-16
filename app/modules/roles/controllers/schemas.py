from pydantic import BaseModel


class PermissionCreate(BaseModel):
    name: str


class PermissionResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class PermissionUpdate(BaseModel):
    name: str

class PermissionUpdateResponse(BaseModel):
    id: int
    name: str

class PermissionDeleteResponse(BaseModel):
    id: int
    name: str

class RoleCreate(BaseModel):
    name: str
    description: str | None = None


class RoleResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True

class RoleUpdate(BaseModel):
    name: str
    description: str | None = None

class RoleUpdateResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

class RoleDeleteResponse(BaseModel):
    id: int
    name: str
    description: str | None = None


class AssignPermission(BaseModel):
    role_id: int
    permission_id: int


class AssignRoleToUser(BaseModel):
    user_id: int
    role_id: int