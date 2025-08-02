from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# Импорт компонентов инфраструктуры
from web_app import models, auth
from web_app.database.repositories.register import RegisterRepository
from web_app.database.connection import db

router = APIRouter(prefix="/auth")

@router.post("/token", response_model=models.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    repo: RegisterRepository = Depends(lambda: RegisterRepository(db))
):
    user = auth.authenticate_user(form_data.username, form_data.password, repo)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(
        data={"sub": user["username"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}