from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os
from app.models import SQLChat, ChatMetaData, MongoChat
from app.services.base import Base

load_dotenv()

# Load MongoDB settings from environment variables
mongo_host = os.getenv("MONGODB_URI")
mongo_db_name = os.getenv("MONGODB_DB")
mongo_port = int(os.getenv("MONGODB_PORT"))

# Load MariaDB settings from environment variables
mariadb_host = os.getenv("MARIADB_HOST")
mariadb_port = int(os.getenv("MARIADB_PORT"))
mariadb_user = os.getenv("MARIADB_USER")
mariadb_password = os.getenv("MARIADB_PASSWORD")
mariadb_db_name = os.getenv("MARIADB_DB")

# MongoDB Setup
mongo_client = MongoClient(mongo_host, mongo_port)
mongo_db = mongo_client[mongo_db_name]
mongo_collection = mongo_db["chats"]

# MariaDB Setup
DATABASE_URL = f"mariadb+pymysql://{mariadb_user}:{mariadb_password}@{mariadb_host}:{mariadb_port}/{mariadb_db_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as e:
        print(f"Error creating tables: {e}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_chat_to_mongo(chat_data: dict):
    chat = MongoChat(**chat_data)
    mongo_collection.insert_one(chat.dict(by_alias=True))
    return chat


def get_chat_from_mongo(role: str):
    result = mongo_collection.find_one({"role": role})
    if result:
        return MongoChat(**result)
    return None


def create_chat(db: Session, content: str, role: str):
    chat_metadata = ChatMetaData(
        mongo_id="some_mongo_id", timestamp="2024-08-13T12:00:00Z", gpt_version="gpt-4"
    )
    db.add(chat_metadata)
    db.commit()
    db.refresh(chat_metadata)

    chat = SQLChat(content=content, role=role, metadata_id=chat_metadata.id)
    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


def get_chat_by_id(db: Session, chat_id: int):
    return db.query(SQLChat).filter(SQLChat.id == chat_id).first()
