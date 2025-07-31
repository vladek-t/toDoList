import sqlite3
from contextlib import contextmanager
from datetime import datetime, date
from typing import List, Dict


class SchemaManager:
    """Менеджер схемы базы данных - создает и мигрирует структуру БД"""
    
    def __init__(self, db_connection: sqlite3.Connection):
        """Инъекция зависимости - передаем соединение с БД извне"""
        self.conn = db_connection
    
    @contextmanager
    def _transaction(self):
        """Контекстный менеджер для безопасной работы с транзакциями"""
        cursor = self.conn.cursor()
        try:
            yield cursor
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise DatabaseError(f"Database transaction failed: {str(e)}") from e
        finally:
            cursor.close()

    def initialize_database(self) -> None:
        """Инициализирует базу данных, создавая все необходимые таблицы"""
        self.create_tasks_table()
        self.create_users_table()
        self._verify_schema_integrity()

    def create_tasks_table(self) -> bool:
        """
        Создает таблицу задач с правильной типизацией для SQLite
        Возвращает True, если таблица была создана (или уже существовала)
        """
        with self._transaction() as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                done INTEGER NOT NULL CHECK(done IN (0, 1)),
                title TEXT NOT NULL CHECK(length(title) > 0),
                due TEXT NOT NULL,  -- Хранение даты в формате ISO8601 (YYYY-MM-DD)
                tech_date_add TEXT NOT NULL,  -- ISO8601 для даты и времени
                tech_date_end TEXT NOT NULL
            )
            ''')
            
            # Проверяем, была ли создана новая таблица
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='tasks'")
            existing_table = cursor.fetchone()
            
            # Добавляем индекс для ускорения поиска по дате
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_due ON tasks(due)")
            
            return "AUTOINCREMENT" in str(existing_table)

    def create_users_table(self) -> bool:
        """
        Создает таблицу пользователей с правильной типизацией и ограничениями
        Возвращает True, если таблица была создана (или уже существовала)
        """
        with self._transaction() as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE CHECK(email LIKE '%_@__%.__%'),
                password TEXT NOT NULL CHECK(length(password) >= 8),
                tech_date_registration TEXT NOT NULL DEFAULT (datetime('now'))
            )
            ''')
            
            # Проверяем существование таблицы
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
            existing_table = cursor.fetchone()
            
            # Добавляем индекс для email
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
            
            return "AUTOINCREMENT" in str(existing_table)

    def _verify_schema_integrity(self) -> None:
        """Проверяет целостность схемы и критические ограничения"""
        with self._transaction() as cursor:
            # Проверяем существование критически важных таблиц
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN ('tasks', 'users')
            """)
            existing_tables = {row[0] for row in cursor.fetchall()}
            
            missing_tables = {'tasks', 'users'} - existing_tables
            if missing_tables:
                raise DatabaseError(f"Critical tables missing: {', '.join(missing_tables)}")
            
            # Проверяем наличие индексов
            cursor.execute("PRAGMA index_list('tasks')")
            task_indexes = {row[1] for row in cursor.fetchall()}
            if 'idx_tasks_due' not in task_indexes:
                cursor.execute("CREATE INDEX idx_tasks_due ON tasks(due)")

    def get_schema_version(self) -> str:
        """Возвращает версию схемы для отслеживания миграций"""
        with self._transaction() as cursor:
            try:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_version (
                    version TEXT PRIMARY KEY,
                    applied_at TEXT NOT NULL DEFAULT (datetime('now'))
                )
                """)
                
                # Проверяем наличие записей
                cursor.execute("SELECT version FROM schema_version ORDER BY applied_at DESC LIMIT 1")
                version = cursor.fetchone()
                
                if not version:
                    # Устанавливаем версию по умолчанию
                    cursor.execute("INSERT INTO schema_version (version) VALUES (?)", ("1.0",))
                    return "1.0"
                
                return version[0]
            except sqlite3.Error as e:
                raise DatabaseError(f"Failed to get schema version: {str(e)}") from e

class DatabaseError(Exception):
    """Кастомное исключение для ошибок работы с БД"""
    pass

class TaskRepository:
    """Репозиторий для работы с задачами (следует паттерну Repository)"""
    
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

    def add_task(
        self,
        done: bool,
        title: str,
        due: date,
        date_add: datetime,
        date_end: datetime
    ) -> int:
        """Добавляет задачу и возвращает её ID"""
        with self._get_cursor() as cursor:
            cursor.execute(
                '''
                INSERT INTO tasks (
                done, 
                title, 
                due, 
                tech_date_add, 
                tech_date_end) 
                VALUES (?, ?, ?, ?, ?)
                ''',
                (int(done), title, due.isoformat(), date_add.isoformat(), date_end.isoformat())
            )
            return cursor.lastrowid

    def get_all_tasks(self) -> List[Dict[str, object]]:
        """Возвращает все задачи в виде списка словарей с правильной типизацией"""
        with self._get_cursor() as cursor:
            cursor.execute('SELECT * FROM tasks')
            columns = [col[0] for col in cursor.description]
            tasks = []
            
            for row in cursor.fetchall():
                task = {}
                for i, col_name in enumerate(columns):
                    value = row[i]
                    
                    # Автоматическая конвертация типов
                    if col_name == "done":
                        task[col_name] = bool(value) if value is not None else None
                    elif col_name in ("due", "tech_date_add", "tech_date_end"):
                        # Конвертируем строки обратно в даты
                        if value:
                            if col_name == "due":
                                task[col_name] = date.fromisoformat(value)
                            else:
                                task[col_name] = datetime.fromisoformat(value)
                        else:
                            task[col_name] = None
                    else:
                        task[col_name] = value
                
                tasks.append(task)
            
            return tasks

    def update_task(
        self,
        task_id: int,
        date_end: datetime,
        done: bool
    ) -> bool:
        """
        Обновляет задачу
        Возвращает True, если задача найдена и обновлена
        """
        with self._get_cursor() as cursor:
            cursor.execute('select id, done from tasks where id = ?', (task_id,))
            row = cursor.fetchone()
            if not row:
                return 'not found'
            
            current_id, current_done = row
            if (int(done) == current_done):
                return 'already done'
            cursor.execute(
            'UPDATE tasks SET done = ?, tech_date_end = ? WHERE id = ?',
            (int(done), date_end.isoformat(), task_id)
            )
            return 'updated' if cursor.rowcount > 0 else 'not updated'

    def delete_task(self, task_id: int) -> bool:
        """
        Удаляет задачу
        Возвращает True, если задача была удалена
        """
        with self._get_cursor() as cursor:
            cursor.execute('SELECT id FROM tasks WHERE id = ?', (task_id,))
            if not cursor.fetchone():
                return 'not found'
            
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            return 'deleted succesfull' if cursor.rowcount > 0 else 'not deleted'