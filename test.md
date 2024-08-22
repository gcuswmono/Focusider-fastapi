# 파일 구조

Python 3.12.4 사용중이고 requirements는 다음과 같아.

```text
aiomysql==0.2.0
annotated-types==0.7.0
anyio==4.4.0
certifi==2024.7.4
cffi==1.17.0
click==8.1.7
cryptography==43.0.0
distro==1.9.0
ecdsa==0.19.0
fastapi==0.112.1
greenlet==3.0.3
h11==0.14.0
httpcore==1.0.5
httpx==0.27.0
idna==3.7
jiter==0.5.0
openai==1.42.0
pyasn1==0.6.0
pycparser==2.22
pydantic==2.8.2
pydantic-settings==2.4.0
pydantic_core==2.20.1
PyMySQL==1.1.1
python-dotenv==1.0.1
python-jose==3.3.0
redis==5.0.8
rsa==4.9
six==1.16.0
sniffio==1.3.1
SQLAlchemy==2.0.32
starlette==0.38.2
tqdm==4.66.5
typing_extensions==4.12.2
uvicorn==0.30.6
```

또한
파일 구조는 다음과 같아

```bash
app
├── __pycache__
│   ├── __init__.cpython-312.pyc
│   ├── database.cpython-312.pyc
│   ├── main.cpython-312.pyc
│   ├── models.cpython-312.pyc
│   ├── redis_client.cpython-312.pyc
│   ├── schemas.cpython-312.pyc
│   └── services.cpython-312.pyc
├── api
│   ├── __init__.py
│   ├── article.py
│   └── chat.py
├── core
│   ├── AuthMiddleware.py
│   ├── __init__.py
│   ├── config.py
│   └── database.py
├── main.py
├── models
│   ├── __init__.py
│   ├── article.py
│   └── chat_history.py
├── redis_client.py
├── schemas
│   ├── article_schemas.py
│   └── chat_schemas.py
└── services
    ├── __init__.py
    ├── article_service.py
    └── chat_service.py
```

모든 __init__.py는 현재는 비어있고 현재 코드는 다음과 같아

```python
# app/api/article.py



# app/api/chat.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.chat_schemas import ChatSchema, ResponseSchema
from app.services.chat_service import handle_chat

router = APIRouter()


@router.post("/chat", response_model=ResponseSchema)
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
        raise HTTPException(status_code=404, detail=str(e))

# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mariadb_user: str
    mariadb_password: str
    mariadb_db: str
    mariadb_host: str
    mariadb_port: int
    redis_host: str
    redis_port: int
    openai_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()


# app/core/database.py
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

# app/models/article.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    level = Column(Integer, nullable=False)
    category = Column(String(30), nullable=False)
    question = Column(String(100), nullable=False)


# app/models/chat_history.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    level = Column(Integer, nullable=False)
    category = Column(String(30), nullable=False)
    question = Column(String(100), nullable=False)

# app/schemas/article_schemas.py
from pydantic import BaseModel


# 기사 관련 응답 데이터 스키마
class ArticleResponseData(BaseModel):
    contents: str  # 기사 내용
    question: str  # 기사에 대한 질문
    article_id: int  # 기사 ID


# 멤버 요청 데이터를 검증하는 스키마
class MemberRequestSchema(BaseModel):
    member_id: int  # 유저의 ID


# 기본 응답 스키마 (필요한 경우 확장 가능)
class ResponseSchema(BaseModel):
    status: int
    message: str
    data: ArticleResponseData


# app/schemas/chat_schemas.py
from pydantic import BaseModel
from typing import Any, Optional


# 기본 응답 스키마
class ResponseSchema(BaseModel):
    status: int
    message: str
    data: Optional[Any]


# 채팅 요청 데이터를 검증하는 스키마
class ChatSchema(BaseModel):
    member_id: int  # 유저의 ID
    article_id: int  # article의 ID
    user_answer: str  # 유저의 답변

# app/services/article_service.py

# app/services/chat_service.py

```
