import sqlite3

conn = sqlite3.connect(r'web_application_base\database\web_tasks_bd.db')
cursor = conn.cursor()

def create_table():
    cursor.execute('''
    create table if not exists tasks (
          id integer primary key
        , done bool not null
        , title text not null
        )
    ''')
    conn.commit()

def add_data(done: bool, title: str):
    cursor.execute('insert into tasks (done, title) values (?, ?)',
                   (done, title))
    conn.commit()

def show_data():
    cursor.execute('select * from tasks')
    all_rows = cursor.fetchall()
    conn.close()
    tasks = []
    for row in all_rows:
        tasks.append({
            'id': row[0],
            'done': bool(row[1]),
            'title': row[2]
        })
    return tasks

def close_connection():
    cursor.close()
    conn.close()