from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(BaseModel):
    password: str
    email: EmailStr
    full_name: str
    roles: list[int] = []

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserResponse(UserBase):
    id: int

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: str | None = None
    roles: list[int] | None = None

    model_config = {"from_attributes": True}


class UserProfileUpdate(BaseModel):
    phone: Optional[str] = Field(
        None,
        pattern=r"^\+?[1-9]\d{9,11}$",
        description="Valid international phone number",
    )
    profile_picture: str | None = None
    full_name: str | None = None

    model_config = {"from_attributes": True}


class UserProfileResponse(UserResponse):
    phone: str | None = None
    profile_picture: str | None = None
    full_name: str | None = None
    email: EmailStr | None = None
    roles: list[int] | None = None

    model_config = {"from_attributes": True}
