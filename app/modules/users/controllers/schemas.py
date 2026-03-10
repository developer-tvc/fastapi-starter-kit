from pydantic import BaseModel,EmailStr




class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserList(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class UserCreate(BaseModel):
    password: str  
    email: EmailStr
    full_name: str

class UserResponse(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }