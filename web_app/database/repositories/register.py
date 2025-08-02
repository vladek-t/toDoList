import sqlite3
from contextlib import contextmanager
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Хеширует пароль с использованием bcrypt"""
    return pwd_context.hash(password)

class RegisterRepository:
    """Репозиторий для работы с регистрацией пользователей (следует паттерну Repository)"""
    
    def __init__(self, db_connection: sqlite3.Connection):
        """Инъекция зависимости - передаем соединение с БД извне"""
        self.conn = db_connection
    
    @contextmanager
    def _get_cursor(self):
        """Контекстный менеджер для безопасной работы с курсором"""
        cursor = self.conn.cursor()
        try:
            yield cursor
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cursor.close()

    def register_user(
            self,
            username: str,
            password: str,
            tech_date_registration: datetime
    ) -> int | None:
        """Регистрирует пользователя и возвращает его ID"""
        with self._get_cursor() as cursor:
            cursor.execute('select username from users where username = ?', (username,))
            row =  cursor.fetchone()
            
            if row:
                return None  # Пользователь уже существует
            
            hashed_password = get_password_hash(password)
            
            cursor.execute(
                '''
                insert into users (
                username, 
                password,
                tech_date_registration)
                values (?, ?, ?)
                ''',
                (username, hashed_password, tech_date_registration.isoformat())
            )
            cursor.execute("SELECT last_insert_rowid()")
            return cursor.fetchone()[0]
        
    def get_all_users(self) -> list[dict[str, object]]:
        """Возвращает всех пользователей в виде списка словарей с правильной типизацией"""
        with self._get_cursor() as cursor:
            cursor.execute('SELECT * FROM users')
            columns = [col[0] for col in cursor.description]
            users = []
            
            for row in cursor.fetchall():
                user = {}
                for i, col_name in enumerate(columns):
                    value = row[i]
                    user[col_name] = value if value is not None else None
                users.append(user)
                
            return users
        
    # В классе RegisterRepository добавьте этот метод
    def get_user_by_username(self, username: str) -> dict | None:
        """Получает пользователя по имени"""
        with self._get_cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            if not row:
                return None
                
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))