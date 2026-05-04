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
    new_task_text = request.form.get('task', '').strip()
    if new_task_text:
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

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """Редактирует задачу по индексу"""
    # Проверка: существует ли задача с таким индексом
    if task_id < 0 or task_id >= len(tasks):
        return "Задача не найдена", 404
    
    # Сохраняем старый текст задачи до изменений
    old_text = tasks[task_id]['text']
    
    if request.method == 'POST':
        # Получаем новый текст из формы
        new_text = request.form.get('task', '').strip()
        
        # ПРОВЕРКА 1: пустое поле
        if new_text == '':
            return render_template('edit.html', 
                                 task=tasks[task_id], 
                                 message="❌ Текст не может быть пустым!")
        
        # ПРОВЕРКА 2: текст не изменился (дополнительное задание)
        if new_text == old_text:
            return render_template('edit.html', 
                                 task=tasks[task_id], 
                                 message="ℹ️ Ничего не изменено. Текст остался тем же.")
        
        # Если все проверки пройдены — сохраняем изменения
        tasks[task_id]['text'] = new_text
        save_tasks(tasks)
        return redirect('/')
    
    # GET-запрос — показываем форму редактирования
    return render_template('edit.html', task=tasks[task_id])

if __name__ == '__main__':
    app.run(debug=True)