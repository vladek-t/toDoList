from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from datetime import datetime
from database import database

app = FastAPI()

# Инициализация БД
database.create_table()

# Модель входных данных
class TaskCreate(BaseModel):
    title: str

class UpdateTask(BaseModel):
    id: int

class DeleteTask(BaseModel):
    id: int


@app.post('/add_task')
async def add_task(task: TaskCreate):
    """Добавление новой задачи через API"""
    try:
        database.add_data(False, task.title, datetime.now(), '9999-01-01 00:00:00.000000')
        return {"message": f"Task '{task.title}' added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/show_tasks')
async def show_tasks():
    all_tasks = database.show_data()
    return all_tasks

@app.put('/update_task')
async def update_task(task: UpdateTask):
    try:
        database.update_task(task.id, datetime.now(), True)
        return {'message': f"Task '{task.id}' update succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete('/delete_task')
async def delete_task(task: DeleteTask):
    try:
        database.delete_task(task.id)
        return {'message': f"Task '{task.id}' delete succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)