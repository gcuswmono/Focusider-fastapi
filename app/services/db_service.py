from pymongo import MongoClient
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

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
Base = declarative_base()

class ChatMetaData(Base):
    __tablename__ = "chat_metadata"

    id = Column(Integer, primary_key=True, index=True)
    mongo_id = Column(String(255), unique=True, index=True)

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
