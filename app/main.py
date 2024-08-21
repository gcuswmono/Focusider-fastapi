from fastapi import FastAPI
from app.api import chat, article

app = FastAPI()

# 도메인별 라우터 설정
app.include_router(chat.router, prefix="/fastapi")
app.include_router(article.router, prefix="/fastapi")
