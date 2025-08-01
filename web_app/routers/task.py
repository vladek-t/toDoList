from fastapi import APIRouter, HTTPException, status
from datetime import datetime

# Импорт компонентов инфораструктуры
from web_app.database.repositories.task import TaskRepository
from web_app.database.connection import db
from web_app import models

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
    return {'message': f"Задача '{task.title}' успешно добавлена с id: {task_add}"}
    
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

    if task_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Такой задачи не существует"
        )

    return {'message': f"Задача '{task.id}' успешно обновлена"}

@router.delete('/delete_task')
async def delete_task(task: models.TaskDelete):
    """Удаление задачи по ID"""
    task_delete = task_repository.delete_task(task_id=task.id)

    if task_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Такой задачи не существует"
        )
    return {'message': f"Task '{task.id}' успешно удалена"}
    