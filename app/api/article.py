from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.article_schemas import (
    ArticleResponseData,
    MemberRequestSchema,
    ResponseSchema,
)
from app.services.article_service import get_random_unseen_article

router = APIRouter()


@router.post("/article/random", response_model=ResponseSchema)
async def get_random_article(
    request: MemberRequestSchema,
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
