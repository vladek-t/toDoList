import sqlite3
import uvicorn
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

# Импорт компонентов инфраструктуры
from web_app.database.schema_manager import SchemaManager
from web_app.routers import task as task_router
from web_app.database.connection import db
from web_app.database.init_db import init_database

# Управление жизненным циклом приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация и очистка ресурсов при запуске/остановке приложения"""
    try:
        init_database()  # Инициализация базы данных        
        yield  # Приложение работает
        
    finally:
        # Здесь можно добавить очистку ресурсов при остановке
        print("Приложение остановлено")

app = FastAPI(
    title="Task Manager API",
    description="API для управления задачами и пользователями",
    version="1.0.0",
    lifespan=lifespan  # Используем управление жизненным циклом
)


# Регистрация роутеров
app.include_router(task_router.router)


# Добавляем обработчик ошибок для базы данных
@app.exception_handler(Exception)
async def database_exception_handler(request, exc):
    if isinstance(exc, sqlite3.DatabaseError):
        return HTTPException(
            status_code=500,
            detail="Ошибка базы данных. Попробуйте позже."
        )
    return HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

if __name__ == "__main__":
    # В production используйте production-сервер (например, gunicorn)
    uvicorn.run(
        "web_app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1,
        loop="asyncio",
        log_level="info"
    )