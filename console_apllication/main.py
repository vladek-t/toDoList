from datetime import datetime
from console_apllication.database import create_table, add_data, close_connection, show_data, update_data, show_id, delete_data, truncate_table

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
    # Извлекаем первый элемент из каждого кортежа
    id_list = [row[0] for row in show_id()]
    task_id = int(input('Номер выполненной задачи: '))
    
    if task_id in id_list:
        update_data(task_id, datetime.now(), True)
    else:
        print('\n⚠️ Задача не найдена')


def delete_task():
    id_list = [row[0] for row in show_id()]
    task_id = int(input('Номер задачи для удаления: '))

    if task_id in id_list:
        delete_data(task_id)
    else:
        print('\n⚠️ Задача не найдена')


def truncate_tasks():
    truncate_table()
    print('\nТаблица очищена')
    

# Основной цикл
while True:
    create_table()

    print('\n1. Добавить задачу\n2. Показать задачи\n' \
    '3. Отметить выполненной\n4. Удалить задачу\n5. Очистка таблицы\n0. Выход')

    try:
        choice = int(input('Выберите действие: '))

        if choice == 1: add_task()
        elif choice == 2: show_tasks()
        elif choice == 3: mark_done()
        elif choice == 4: delete_task()
        elif choice == 5: truncate_tasks()
        elif choice == 0: 
            close_connection()
            break
    
    except ValueError as e:
        print('Ошибка: ', e)
