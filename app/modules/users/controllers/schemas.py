from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)

    @field_validator("full_name")
    def normalize_full_name(cls, v):
        if v:
            return v.strip()
        return v


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=1, max_length=100)
    roles: list[int] = []

    @field_validator("email")
    def normalize_email(cls, v):
        return v.lower().strip()

    @field_validator("password")
    def validate_password(cls, v):
        if not (8 <= len(v) <= 128):
            raise ValueError("Password must be between 8 and 128 characters")
        return v

    @field_validator("full_name")
    def normalize_full_name(cls, v):
        return v.strip()


class UserResponse(UserBase):
    id: int

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    roles: list[int] | None = None

    @field_validator("full_name")
    def normalize_full_name(cls, v):
        if v:
            return v.strip()
        return v

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
