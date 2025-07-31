import os
import sqlite3
from pathlib import Path
from fastapi import APIRouter, HTTPException
from datetime import datetime
from web_app.database.database import TaskRepository
from dotenv import load_dotenv
from datetime import date

# Импорт компонентов инфораструктуры
from web_app import models

load_dotenv(Path(__file__).parent.parent.parent / ".env")

database = os.getenv("DATABASE")
db = sqlite3.connect(database)

router = APIRouter(prefix='/task')

task_repository = TaskRepository(db)

@router.post('/add_task')
async def add_task(task: models.TaskCreate):
    """Добавление новой задачи через API"""
    task_add = task_repository.add_task(
        done=False,
        due=task.due,
        title=task.title,
        date_add=datetime.now(),
        date_end=datetime(9999, 1, 1, 0, 0, 0, 0)
    )
    return {'message': f"Task '{task.title}' added successfully with ID {task_add}"}
    
@router.get('/show_tasks')
async def show_tasks():
    """Получение всех задач"""
    return task_repository.get_all_tasks()

@router.put('/update_task')
async def update_task(task: models.TaskUpdate):
    """Обновление задачи по ID"""
    task_update = task_repository.update_task(
        task_id=task.id,
        date_end=datetime.now(),
        done=True
    )
    return {'message': f"Task '{task.id}' {task_update}"}

@router.delete('/delete_task')
async def delete_task(task: models.TaskDelete):
    """Удаление задачи по ID"""
    task_delete = task_repository.delete_task(task_id=task.id)
    return {'message': f"Task '{task.id}' {task_delete}"}
    