# app/schemas.py

from pydantic import BaseModel
from typing import Any, Optional


# 기본 응답 스키마
class ResponseSchema(BaseModel):
    status: int
    message: str
    data: Optional[Any]


# 특정 응답 데이터 스키마 (예: article의 정보)
class ArticleResponseData(BaseModel):
    contents: str
    question: str
    article_id: int


class MemberRequestSchema(BaseModel):
    member_id: int


# ChatSchema: 유저의 채팅 요청 데이터를 검증하는 Pydantic 스키마
class ChatSchema(BaseModel):
    member_id: int  # 유저의 ID
    article_id: int  # article의 ID
    user_answer: str  # 유저의 답변
