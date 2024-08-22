from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.chat_schemas import ChatSchema
from app.schemas.common_schemas import ResponseSchema
from app.services.chat_service import handle_chat

router = APIRouter()


@router.post("/chat", response_model=ResponseSchema)
async def chat_with_gpt(chat_data: ChatSchema, db: AsyncSession = Depends(get_db)):
    try:
        gpt_response = await handle_chat(
            chat_data.member_id, chat_data.article_id, chat_data.user_answer, db
        )
        return {
            "status": 200,
            "message": "성공했습니다.",
            "data": {"gpt_response": gpt_response},
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
