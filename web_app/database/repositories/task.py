import sqlite3
from contextlib import contextmanager
from datetime import datetime, date
from typing import List, Dict

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
    ) -> int | None:
        """
        Обновляет задачу
        Возвращает True, если задача найдена и обновлена
        """
        with self._get_cursor() as cursor:
            cursor.execute('select id, done from tasks where id = ?', (task_id,))
            row = cursor.fetchone()
            if not row:
                return None
            
            current_id, current_done = row
            if (int(done) == current_done):
                return 'already done'
            cursor.execute(
            'UPDATE tasks SET done = ?, tech_date_end = ? WHERE id = ?',
            (int(done), date_end.isoformat(), task_id)
            )
            cursor.execute("SELECT last_insert_rowid()")
            return cursor.fetchone()[0]

    def delete_task(self, task_id: int) -> int | None:
        """
        Удаляет задачу
        Возвращает True, если задача была удалена
        """
        with self._get_cursor() as cursor:
            cursor.execute('SELECT id FROM tasks WHERE id = ?', (task_id,))
            row = cursor.fetchone()
            if not row:
                return None
            
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            return cursor.fetchone()[0]