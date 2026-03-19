from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    total: int
    next: Optional[str]
    previous: Optional[str]
    data: List[T]
    

    