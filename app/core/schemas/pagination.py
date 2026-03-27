from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    total: int
    next: Optional[str]
    previous: Optional[str]
    data: List[T]
