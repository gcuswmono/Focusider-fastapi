# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services import get_random_unseen_article, gpt_generate_response, handle_chat
from app.schemas import (
    ChatSchema,
    ResponseSchema,
    ArticleResponseData,
    MemberRequestSchema,
)


app = FastAPI()


# 테스트용 GPT API 스키마 정의
class GPTTestSchema(BaseModel):
    prompt: str  # 유저가 보낼 프롬프트

# GPT-4 모델을 테스트하는 API
@app.post("/fastapi/gpt-test", response_model=ResponseSchema)
async def gpt_test(data: GPTTestSchema):
    try:
        # 간단한 프롬프트로 GPT 호출
        response = await gpt_generate_response(data.prompt)
        return {
            "status": 200,
            "message": "GPT 테스트 성공",
            "data": {"gpt_response": response},
        }
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

# 채팅 API: 유저의 답변을 GPT에게 보내고 다음 질문을 생성하는 API
@app.post("/fastapi/chat", response_model=ResponseSchema)
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
        print(e)
        raise HTTPException(status_code=404, detail=str(e))


# 유저가 아직 본 적 없는 랜덤 article을 반환하는 API
@app.post("/fastapi/article/random", response_model=ResponseSchema)
async def get_random_article(
    request: MemberRequestSchema,  # Request body에서 member_id를 받음
    db: AsyncSession = Depends(get_db),
):
    try:
        article = await get_random_unseen_article(request.member_id, db)
        return {
            "status": 200,
            "message": "성공했습니다.",
            "data": ArticleResponseData(
                contents=article.content,
                question=article.question,
                article_id=article.id,
            ),
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
