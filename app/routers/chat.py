# routers/chat.py
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.schemas import ChatRequest, ChatResponse
from app.services.gpt_service import call_gpt_api

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    try:
        messages = [{"role": msg.role, "content": msg.content} for msg in chat_request.messages]
        response = await call_gpt_api(messages)
        reply = response.get("choices")[0].get("message").get("content")
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
