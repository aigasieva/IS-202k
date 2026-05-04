from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

FILE_NAME = 'tasks.json'

def load_tasks():
    """Загружает задачи из JSON-файла"""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Сохраняет задачи в JSON-файл"""
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# Загружаем задачи при старте приложения
tasks = load_tasks()

@app.route('/')
def index():
    """Главная страница — показывает список задач"""
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Добавляет новую задачу с текущей датой"""
    new_task_text = request.form['task']
    if new_task_text:
        # Создаём задачу как словарь с текстом и датой
        new_task = {
            'text': new_task_text,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        tasks.append(new_task)
        save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Удаляет задачу по индексу"""
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect('/')

@app.route('/clear')
def clear_all():
    """Очищает все задачи"""
    tasks.clear()
    save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)