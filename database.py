import sqlite3
from datetime import datetime

conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

def close_connection():
    cursor.close()
    conn.close()

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
    cursor.execute("select * from tasks")
    all_rows = cursor.fetchall()
    for row in all_rows:
        print(row, '\n')
