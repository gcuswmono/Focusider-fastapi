# app/models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    level = Column(Integer, nullable=False)
    category = Column(String(30), nullable=False)
    question = Column(String(100), nullable=False)


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_id = Column(Integer, nullable=False)
    chat = Column(Text, nullable=False)
    article_id = Column(Integer, ForeignKey("article.id"), nullable=False)
