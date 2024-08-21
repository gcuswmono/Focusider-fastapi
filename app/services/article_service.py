import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.models.article import Article


async def get_random_unseen_article(member_id: int, db: AsyncSession):
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

    unseen_articles = (
        await db.execute(
            text("SELECT * FROM article WHERE id NOT IN :seen_articles"),
            {"seen_articles": tuple(seen_articles) if seen_articles else (-1,)},
        )
    ).all()

    if not unseen_articles:
        raise ValueError("No unseen articles available for this user.")

    return random.choice(unseen_articles)
