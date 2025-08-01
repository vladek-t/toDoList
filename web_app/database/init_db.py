from pathlib import Path

from web_app.database.connection import db

def init_database():
    """Инициализация базы данных из SQL-скрипта"""
    print("Инициализация базы данных...")
    init_sql_path = Path("web_app/database/init.sql")

    if not init_sql_path.exists():
        raise RuntimeError("Файл database/init.sql не найден!")
    
    # Чтение SQL-скрипта
    with open(init_sql_path, "r", encoding="utf-8") as f:
        sql_commands = f.read().split(";")
    
    try:
        conn = db
        cursor = conn.cursor()

        with open(init_sql_path, "r", encoding="utf-8") as f:
            sql_script = f.read()

        cursor.executescript(sql_script)
        conn.commit()
        print("База данных успешно инициализирована из init.sql")
    
    except Exception as e:
        print(f"Ошибка инициализации базы данных: {e}")
        raise