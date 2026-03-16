from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserList(UserBase):
    id: int

    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    password: str
    email: EmailStr
    full_name: str
    roles: list[int] = []


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
