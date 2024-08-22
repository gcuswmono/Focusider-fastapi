from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    level = Column(Integer, nullable=False)
    category = Column(String(30), nullable=False)
    question = Column(String(100), nullable=False)
