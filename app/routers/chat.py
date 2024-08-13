from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import ChatRequest, ChatResponse
from app.services.gpt_service import call_gpt_api
from app.services.db_service import (
    create_chat,
    get_chat_by_id,
    get_db,
    save_chat_to_mongo,
    get_chat_from_mongo,
)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    try:
        messages = [
            {"role": msg.role, "content": msg.content} for msg in chat_request.messages
        ]
        response = await call_gpt_api(messages)
        reply = response.get("choices")[0].get("message").get("content")
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save_chat", response_model=ChatResponse)
async def save_chat(chat_request: ChatRequest):
    chat_data = {
        "role": chat_request.messages[0].role,
        "content": chat_request.messages[0].content,
    }
    saved_chat = save_chat_to_mongo(chat_data)
    return ChatResponse(reply="Chat saved successfully!")


@router.get("/get_chat", response_model=ChatResponse)
async def get_chat(role: str):
    chat = get_chat_from_mongo(role)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return ChatResponse(reply=chat.content)


@router.post("/save_chat_to_db", response_model=ChatResponse)
def save_chat_to_db(chat_request: ChatRequest, db: Session = Depends(get_db)):
    chat = create_chat(
        db, content=chat_request.messages[0].content, role=chat_request.messages[0].role
    )
    return ChatResponse(reply="Chat saved to MariaDB successfully!")


@router.get("/get_chat_from_db/{chat_id}", response_model=ChatResponse)
def get_chat_from_db(chat_id: int, db: Session = Depends(get_db)):
    chat = get_chat_by_id(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return ChatResponse(reply=chat.content)
