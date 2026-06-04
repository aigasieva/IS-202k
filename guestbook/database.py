import sqlite3
from datetime import date

DATABASE = 'guestbook.db'

def get_db_connection():
    """Устанавливает соединение с базой данных"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по имени
    return conn

def init_db():
    """Создаёт таблицу messages, если её нет"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("База данных инициализирована")

def get_all_messages():
    """Возвращает все сообщения, отсортированные от новых к старым"""
    conn = get_db_connection()
    messages = conn.execute(
        'SELECT * FROM messages ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    return messages

def add_test_messages():
    """Добавляет тестовые сообщения (только для проверки)"""
    conn = get_db_connection()
    
    # Проверяем, есть ли уже сообщения
    count = conn.execute('SELECT COUNT(*) FROM messages').fetchone()[0]
    
    if count == 0:
        test_messages = [
            ('Айразиева Исхакова', 'Привет всем! Это моя гостевая книга!', '2026-06-04'),
            ('Анна', 'Отличный проект!', '2026-06-03'),
            ('Иван', 'Жду продолжения!', '2026-06-02'),
            ('Мария', 'Очень полезная работа', '2026-06-01')
        ]
        conn.executemany(
            'INSERT INTO messages (name, message, created_at) VALUES (?, ?, ?)',
            test_messages
        )
        conn.commit()
        print("Тестовые сообщения добавлены")
    
    conn.close()
