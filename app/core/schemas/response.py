"""
APIResponse is a generic response class that can be used to return data from the API.
"""
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel


T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """
    APIResponse is a generic response class that can be used to return data from the API.
    """
    success: bool
    message: str
    data: Optional[T] = None

    @staticmethod
    def success_response(data=None, message="Success"):
        """
        Returns a success response.
        """
        return APIResponse(success=True, message=message, data=data)
