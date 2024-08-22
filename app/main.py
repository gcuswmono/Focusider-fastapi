from fastapi import Depends, FastAPI, HTTPException
from app.api import chat, article
from app.core.database import get_db
from app.schemas.article_schemas import ArticleResponseData, MemberRequestSchema
from app.schemas.chat_schemas import ChatSchema
from app.schemas.common_schemas import ResponseSchema
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.common_schemas import ResponseSchema
from app.services.article_service import get_random_unseen_article
from app.services.chat_service import handle_chat

app = FastAPI()

# 도메인별 라우터 설정
app.include_router(chat.router, prefix="/fastapi")
app.include_router(article.router, prefix="/fastapi")
