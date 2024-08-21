from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

DATABASE_URL = f"mysql+aiomysql://{settings.mariadb_user}:{settings.mariadb_password}@{settings.mariadb_host}:{settings.mariadb_port}/{settings.mariadb_db}"

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
