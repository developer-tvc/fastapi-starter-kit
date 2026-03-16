from pydantic import BaseModel


class NotificationList(BaseModel):
    id: int
    user_id: int
    title: str
    message: str

    class Config:
        from_attributes = True
