from fastapi import FastAPI
from app.routers import chat
from app.services.db_service import create_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables()

app.include_router(chat.router, prefix="/api")