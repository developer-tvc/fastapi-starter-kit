from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None

    @staticmethod
    def success_response(data=None, message="Success"):
        return APIResponse(success=True, message=message, data=data)
