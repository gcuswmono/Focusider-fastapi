# schemas.py
from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    start_conversation: Optional[bool] = False
    end_conversation: Optional[bool] = False

class ChatResponse(BaseModel):
    reply: str
