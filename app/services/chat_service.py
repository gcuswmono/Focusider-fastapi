import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.chat_history import ChatHistory
from app.redis_client import redis_client


async def handle_chat(
    member_id: int, article_id: int, user_answer: str, db: AsyncSession
):
    state = await get_chat_state(member_id, article_id)
    # 상태에 따라 적절한 GPT 응답 생성 및 채팅 상태 관리 로직
    # Redis 또는 DB 저장 처리 등...
    pass
