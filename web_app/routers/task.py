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
        date_end='9999-01-01 00:00:00.000000'
    )
    return task_add
    # return {"message": f"Task '{task.title}' added successfully"}
    # """Добавление новой задачи через API"""
    # try:
    #     database.Tasks.add_task(False, task.title, task.due, datetime.now(), '9999-01-01 00:00:00.000000')
    #     return {"message": f"Task '{task.title}' added successfully"}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/show_tasks')
async def show_tasks():
    return task_repository.get_all_tasks()
    # all_tasks = database.Tasks.show_tasks()
    # return all_tasks

@router.put('/update_task')
async def update_task(task: models.TaskUpdate):
    try:
        id_list = [row[0] for row in database.Tasks.show_tasks_id()]
        
        if task.id in id_list:
            database.Tasks.update_task(task.id, datetime.now(), True)
            return {'message': f"Task '{task.id}' update succesfully"}
        else:
            return {'message': f"Task '{task.id}' doesn't exists"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/delete_task')
async def delete_task(task: models.TaskDelete):
    try:
        id_list = [row[0] for row in database.Tasks.show_tasks_id()]

        if task.id in id_list:
            database.Tasks.delete_task(task.id)
            return {'message': f"Task '{task.id}' delete succesfully"}
        else:
            return {'message': f"Task '{task.id}' doesn't exists"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))