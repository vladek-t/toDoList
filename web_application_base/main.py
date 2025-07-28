from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from database import database

app = FastAPI()

# Инициализация БД
database.create_table()

# Модель входных данных
class TaskCreate(BaseModel):
    title: str

@app.post('/add')
async def add_task(task: TaskCreate):
    """Добавление новой задачи через API"""
    try:
        database.add_data(False, task.title)
        return {"message": f"Task '{task.title}' added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)