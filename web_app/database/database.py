import sqlite3
from datetime import datetime

conn = sqlite3.connect(r'web_app\database\web_tasks_bd.db')
cursor = conn.cursor()


def create_table():
    cursor.execute('''
    create table if not exists tasks (
          id integer primary key
        , done bool not null
        , title text not null
        , date_add datetime not null
        , date_end datetime not null
        )
    ''')
    conn.commit()


def add_data(done: bool, title: str, date_add: datetime, date_end: datetime):
    cursor.execute('insert into tasks (done, title, date_add, date_end) values (?, ?, ?, ?)',
                   (done, title, date_add, date_end))
    conn.commit()


def show_data():
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()
    
    # Получаем названия столбцов
    columns = [col[0] for col in cursor.description]
    
    # Преобразуем каждую строку в словарь с обработкой булевых значений
    result = []
    for row in rows:
        row_dict = {}
        for i, col_name in enumerate(columns):
            value = row[i]
            
            # Специальная обработка для поля 'done'
            if col_name == 'done':
                # Преобразуем 0/1 в булевы значения
                row_dict[col_name] = bool(value) if value is not None else None
            else:
                row_dict[col_name] = value
                
        result.append(row_dict)
    
    return result


def update_task(id: int, date_end: datetime, done: bool):
    cursor.execute('update tasks set done = ?, date_end = ? where id = ?', 
                   (done, date_end, id))
    conn.commit()


def delete_task(id: int):
    cursor.execute('delete from tasks where id = ?', (id,))
    conn.commit()