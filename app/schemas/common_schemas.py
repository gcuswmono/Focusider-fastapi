from typing import Any, Optional
from pydantic import BaseModel


# 기본 응답 스키마
class ResponseSchema(BaseModel):
    status: int
    message: str
    data: Optional[Any]
