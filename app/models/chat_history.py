from sqlalchemy import Column, Integer, Text, ForeignKey
from app.core.database import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_id = Column(Integer, nullable=False)
    chat = Column(Text, nullable=False)
    article_id = Column(Integer, ForeignKey("article.id"), nullable=False)
