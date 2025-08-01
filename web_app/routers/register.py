from fastapi import APIRouter, HTTPException, status
from datetime import datetime

# Импорт компонентов инфораструктуры
from web_app.database.repositories.register import RegisterRepository
from web_app.database.connection import db
from web_app import models

router = APIRouter(prefix='/register')

register_repository = RegisterRepository(db)

@router.post('/register_user')
async def register_user(user: models.UserCreate):
    """Регистрация нового пользователя через API"""
    tech_date_registration = datetime.now()
    user_id = register_repository.register_user(
        username=user.username,
        password=user.password,
        tech_date_registration=tech_date_registration
    )

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким именем уже существует'
        )
    
    return {'message': f"User '{user.username}' registered successfully"}