from pydantic import BaseModel
from datetime import date

class TaskCreate(BaseModel):
    title: str
    due: date

class TaskUpdate(BaseModel):
    id: int

class TaskDelete(BaseModel):
    id: int
