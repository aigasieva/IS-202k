import sqlite3
from datetime import date

DATABASE = 'guestbook.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
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
    print("База данных готова")

def get_all_messages(sort_order='DESC'):
    """Возвращает все сообщения с сортировкой по дате"""
    conn = get_db_connection()
    messages = conn.execute(
        f'SELECT * FROM messages ORDER BY created_at {sort_order}'
    ).fetchall()
    conn.close()
    return messages

def add_message(name, message):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO messages (name, message, created_at) VALUES (?, ?, ?)',
        (name, message, date.today().strftime('%Y-%m-%d'))
    )
    conn.commit()
    conn.close()

def delete_message(message_id):
    """Удаляет сообщение по id"""
    conn = get_db_connection()
    conn.execute('DELETE FROM messages WHERE id = ?', (message_id,))
    conn.commit()
    conn.close()

def delete_all_messages():
    """Удаляет все сообщения"""
    conn = get_db_connection()
    conn.execute('DELETE FROM messages')
    conn.commit()
    conn.close()

def get_message_count():
    """Возвращает количество сообщений"""
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(*) FROM messages').fetchone()[0]
    conn.close()
    return count
