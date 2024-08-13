# app/models.py

from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.services.base import Base

# Pydantic 모델
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema):
        schema.update(type="string")
        return schema


class MongoChat(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    role: str
    content: str
    timestamp: Optional[str] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# SQLAlchemy 모델
class ChatMetaData(Base):
    __tablename__ = "chat_metadata"

    id = Column(Integer, primary_key=True, index=True)
    mongo_id = Column(String(255), unique=True, index=True)
    timestamp = Column(String(255))
    gpt_version = Column(String(255))

    related_chat = relationship("SQLChat", back_populates="chat_metadata")


class SQLChat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255))
    role = Column(String(50))
    metadata_id = Column(Integer, ForeignKey("chat_metadata.id"))

    chat_metadata = relationship("ChatMetaData", back_populates="related_chat")
