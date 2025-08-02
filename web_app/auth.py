from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

# Импорт компонентов инфраструктуры
from web_app.database.repositories.register import RegisterRepository, pwd_context
from web_app.database.connection import db

# Настройки JWT
SECRET_KEY = "YOUR_SECRET_KEY"  # Замените на надежный ключ в .env!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def authenticate_user(username: str, password: str, repo: RegisterRepository):
    """Проверяет учетные данные пользователя"""
    user = repo.get_user_by_username(username)
    if not user:
        return False
    if not pwd_context.verify(password, user["password"]):
        return False
    return user

def create_access_token(data: dict):
    """Создает JWT токен с правильной временной зоной"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    repo: RegisterRepository = Depends(lambda: RegisterRepository(db))
):
    """Получает текущего пользователя из токена"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    user = repo.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user