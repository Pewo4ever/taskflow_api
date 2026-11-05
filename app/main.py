import logging
from app.config import settings
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.routers import users, projects, labels, tasks, comments

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="TaskFlow API",
    description="REST API для управления задачами команды",
    version="1.0.0"
)

# Подключаем все роутеры
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(labels.router)
app.include_router(tasks.router)
app.include_router(comments.router)


@app.get("/health", tags=["System"])
def health_check(db: Session = Depends(get_db)):
    """Проверка соединения с базой данных"""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")


@app.get("/", tags=["System"])
def root():
    return {"message": "Welcome to TaskFlow API! Check /docs for documentation."}