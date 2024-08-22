from pydantic import BaseModel
from typing import Any, Optional


# 채팅 요청 데이터를 검증하는 스키마
class ChatSchema(BaseModel):
    member_id: int  # 유저의 ID
    article_id: int  # article의 ID
    user_answer: str  # 유저의 답변
