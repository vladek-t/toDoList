import sqlite3
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pathlib import Path
from dotenv import load_dotenv

# Импорт компонентов инфраструктуры
from web_app.database.database import SchemaManager
from web_app.routers import task as task_router


load_dotenv(Path(__file__).parent.parent / ".env")

database = os.getenv("DATABASE")
db = sqlite3.connect(database)

# Управление жизненным циклом приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация и очистка ресурсов при запуске/остановке приложения"""
    try:
        # Инициализация базы данных при старте
        print("Инициализация базы данных...")
        schema_manager = SchemaManager(db)
        schema_manager.initialize_database()
        print("База данных успешно инициализирована")
        
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


# Инициализация БД
# database.CreateTable.create_table_tasks()
# database.CreateTable.create_table_users()

# app = FastAPI()


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)