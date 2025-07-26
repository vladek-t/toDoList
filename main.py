from datetime import datetime

class Task:
    def __init__(self, id: int, title: str, done: bool, date_added: datetime, date_end: datetime):
        self.id = id
        self.title = title
        self.done = done
        self.date_added = date_added
        self.date_end = date_end

tasks = []
next_id = 1

def add_task():
    global next_id
    title = input("Введите задачу: ")
    tasks.append(Task(next_id, title, False, datetime.now(), '9999-01-01 00:00:00.000000'))
    # tasks.append({"id": next_id, "title": title, "done": False})
    next_id += 1
    print("✅ Задача добавлена!")

def show_tasks():
    print("\n--- Список задач ---")
    print("id, done, title, Date Add, Date End")
    for task in tasks:
        status = "✓" if task.done == True else "X"
        print(f"{task.id}. {status} {task.title}, {task.date_added}, {task.date_end}")
        # print(f"{task['id']}. [{status}] {task['title']}")

def mark_done():
    task_id = int(input("Номер выполненной задачи: "))
    for task in tasks:
        if task.id == task_id:
            task.done = True
            task.date_end = datetime.now()
            print("✅ Задача отмечена как выполненная")
            return
    print("⚠️ Задача не найдена")
    

# Основной цикл
while True:
    print("\n1. Добавить задачу\n2. Показать задачи\n3. Отметить выполненной\n0. Выход")
    choice = input("Выберите действие: ")
    
    if choice == "1": add_task()
    elif choice == "2": show_tasks()
    elif choice == "3": mark_done()
    elif choice == "0": break
