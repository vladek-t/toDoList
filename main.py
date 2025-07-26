from datetime import datetime
from database import create_table, add_data, close_connection, show_data, update_data

class Task:
    def __init__(self, id: int, title: str, done: bool, date_added: datetime, date_end: datetime):
        self.id = id
        self.title = title
        self.done = done
        self.date_added = date_added
        self.date_end = date_end


def add_task():
    title = input('Введите задачу: ')
    add_data(False, title, datetime.now(), '9999-01-01 00:00:00.000000')
    print('✅ Задача добавлена!')


def show_tasks():
    print('\n--- Список задач ---')
    show_data()


def mark_done():
    task_id = int(input('Номер выполненной задачи: '))
    update_data(task_id, datetime.now(), True)

    # for task in tasks:
    #     if task.id == task_id:
    #         task.done = True
    #         task.date_end = datetime.now()
    #         print('✅ Задача отмечена как выполненная')
    #         return
    # print('⚠️ Задача не найдена')
    

# Основной цикл
while True:
    create_table()

    print('\n1. Добавить задачу\n2. Показать задачи\n3. Отметить выполненной\n0. Выход')
    choice = input('Выберите действие: ')
    
    if choice == '1': add_task()
    elif choice == '2': show_tasks()
    elif choice == '3': mark_done()
    elif choice == '0': 
        close_connection()
        break
