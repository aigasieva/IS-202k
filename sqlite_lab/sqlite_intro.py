import sqlite3

# ==================== ЗАДАНИЕ 2-9 ====================
# Подключаемся к базе данных (файл mybase.db)
conn = sqlite3.connect('mybase.db')
cursor = conn.cursor()

print("База данных создана и подключена!")

# Задание 3. Создаём таблицу users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
''')
conn.commit()
print("Таблица users создана!")

# Задание 4. Добавляем данные (INSERT)
# Добавляем одного пользователя
cursor.execute('''
    INSERT INTO users (name, age) VALUES (?, ?)
''', ('Анна', 25))

# Добавляем нескольких пользователей
users = [
    ('Иван', 30),
    ('Мария', 22),
    ('Петр', 35)
]
cursor.executemany('INSERT INTO users (name, age) VALUES (?, ?)', users)
conn.commit()
print("Пользователи добавлены!")

# Задание 5. Читаем данные (SELECT)
cursor.execute('SELECT * FROM users')
all_users = cursor.fetchall()

print("\n--- Все пользователи ---")
for user in all_users:
    print(f"id: {user[0]}, имя: {user[1]}, возраст: {user[2]}")

# Задание 6. Читаем данные с условием WHERE
cursor.execute('SELECT * FROM users WHERE age > 25')
older_users = cursor.fetchall()

print("\n--- Пользователи старше 25 ---")
for user in older_users:
    print(f"id: {user[0]}, имя: {user[1]}, возраст: {user[2]}")

# Задание 7. Изменяем данные (UPDATE)
cursor.execute('UPDATE users SET age = age + 1')
conn.commit()

cursor.execute('SELECT * FROM users')
updated_users = cursor.fetchall()

print("\n--- После увеличения возраста ---")
for user in updated_users:
    print(f"id: {user[0]}, имя: {user[1]}, возраст: {user[2]}")

# Задание 8. Удаляем данные (DELETE)
cursor.execute('DELETE FROM users WHERE id = ?', (2,))
conn.commit()

cursor.execute('SELECT * FROM users')
remaining_users = cursor.fetchall()

print("\n--- После удаления id=2 ---")
for user in remaining_users:
    print(f"id: {user[0]}, имя: {user[1]}, возраст: {user[2]}")

# Задание 9. Закрываем соединение
conn.close()
print("\nСоединение закрыто.")


# ==================== ЗАДАНИЕ 10-17 ====================
# Открываем новое соединение для работы с products
print("\n" + "="*50)
print("РАБОТА С ТАБЛИЦЕЙ products")
print("="*50)

conn = sqlite3.connect('mybase.db')
cursor = conn.cursor()

# Задание 10. Создаём таблицу products
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        quantity INTEGER DEFAULT 0
    )
''')
conn.commit()
print("Таблица products создана!")

# Задание 11. Добавляем товары
products = [
    ('Яблоки', 50, 100),
    ('Бананы', 80, 50),
    ('Молоко', 70, 30),
    ('Хлеб', 40, 0),
    ('Сыр', 150, 20)
]
cursor.executemany('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)', products)
conn.commit()
print("Товары добавлены!")

# Задание 12. Выводим все товары
cursor.execute('SELECT * FROM products')
all_products = cursor.fetchall()

print("\n--- Все товары ---")
for product in all_products:
    print(f"{product[0]}. {product[1]} - {product[2]} руб, в наличии: {product[3]}")

# Задание 13. Товары с ценой меньше 100 рублей
cursor.execute('SELECT * FROM products WHERE price < 100')
cheap_products = cursor.fetchall()

print("\n--- Товары дешевле 100 руб ---")
for product in cheap_products:
    print(f"{product[1]} - {product[2]} руб")

# Задание 14. Товары, которых нет в наличии (quantity = 0)
cursor.execute('SELECT * FROM products WHERE quantity = 0')
out_of_stock = cursor.fetchall()

print("\n--- Товары, которых нет в наличии ---")
for product in out_of_stock:
    print(f"{product[1]}")

# Задание 15. Увеличиваем цену всех товаров на 10 рублей
cursor.execute('UPDATE products SET price = price + 10')
conn.commit()

cursor.execute('SELECT * FROM products')
updated_products = cursor.fetchall()

print("\n--- После увеличения цены на 10 руб ---")
for product in updated_products:
    print(f"{product[1]} - {product[2]} руб, в наличии: {product[3]}")

# Задание 16. Удаляем товары с ценой выше 100 рублей
cursor.execute('DELETE FROM products WHERE price > 100')
conn.commit()

cursor.execute('SELECT * FROM products')
after_delete = cursor.fetchall()

print("\n--- После удаления товаров дороже 100 руб ---")
for product in after_delete:
    print(f"{product[1]} - {product[2]} руб, в наличии: {product[3]}")

# Задание 17. Добавляем поле category
cursor.execute('ALTER TABLE products ADD COLUMN category TEXT DEFAULT "другое"')
conn.commit()
print("\nПоле category добавлено!")

# Заполняем категории
categories = [
    ('Яблоки', 'фрукты'),
    ('Бананы', 'фрукты'),
    ('Молоко', 'молочные'),
    ('Хлеб', 'выпечка')
]

for product_name, category in categories:
    cursor.execute('UPDATE products SET category = ? WHERE name = ?', (category, product_name))
conn.commit()

# Выводим итоговую таблицу
cursor.execute('SELECT * FROM products')
final_products = cursor.fetchall()

print("\n--- Итоговая таблица products с категориями ---")
for product in final_products:
    print(f"{product[1]} - {product[2]} руб, в наличии: {product[3]}, категория: {product[4]}")

# Закрываем соединение
conn.close()
print("\nСоединение закрыто.")