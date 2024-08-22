import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.models.article import Article


async def get_random_unseen_article(member_id: int, db: AsyncSession):
    # 사용자가 본 article_id 목록을 가져옴
    seen_articles = (
        (
            await db.execute(
                text(
                    "SELECT article_id FROM chat_history WHERE member_id = :member_id"
                ),
                {"member_id": member_id},
            )
        )
        .scalars()
        .all()
    )

    # seen_articles가 비어 있는 경우 빈 튜플 대신 (-1,)로 처리
    seen_articles_tuple = tuple(seen_articles) if seen_articles else (-1,)

    # 사용자가 본 적 없는 article을 가져옴
    unseen_articles = (
        await db.execute(
            text("SELECT * FROM article WHERE id NOT IN :seen_articles"),
            {"seen_articles": seen_articles_tuple},
        )
    ).fetchall()

    if not unseen_articles:
        raise ValueError("No unseen articles available for this user.")

    # 랜덤으로 하나의 unseen article을 반환
    return random.choice(unseen_articles)
