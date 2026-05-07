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
    """Главная страница — показывает все задачи"""
    return render_template('index.html', tasks=tasks, filter_type='all')

@app.route('/active')
def show_active():
    """Показывает только НЕвыполненные задачи (done = false)"""
    active_tasks = [task for task in tasks if not task.get('done', False)]
    return render_template('index.html', tasks=active_tasks, filter_type='active')

@app.route('/completed')
def show_completed():
    """Показывает только выполненные задачи (done = true)"""
    completed_tasks = [task for task in tasks if task.get('done', False)]
    return render_template('index.html', tasks=completed_tasks, filter_type='completed')

@app.route('/add', methods=['POST'])
def add_task():
    """Добавляет новую задачу с текущей датой и done=False"""
    new_task_text = request.form.get('task', '').strip()
    if new_task_text:
        new_task = {
            'text': new_task_text,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'done': False
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

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    """Переключает статус выполнения задачи (done True/False)"""
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = not tasks[task_id].get('done', False)
        save_tasks(tasks)
    return redirect('/')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """Редактирует задачу по индексу"""
    if task_id < 0 or task_id >= len(tasks):
        return "Задача не найдена", 404
    
    old_text = tasks[task_id]['text']
    
    if request.method == 'POST':
        new_text = request.form.get('task', '').strip()
        
        if new_text == '':
            return render_template('edit.html', 
                                 task=tasks[task_id], 
                                 message="❌ Текст не может быть пустым!")
        
        if new_text == old_text:
            return render_template('edit.html', 
                                 task=tasks[task_id], 
                                 message="ℹ️ Ничего не изменено. Текст остался тем же.")
        
        tasks[task_id]['text'] = new_text
        save_tasks(tasks)
        return redirect('/')
    
    return render_template('edit.html', task=tasks[task_id])

@app.route('/clear')
def clear_all():
    """Очищает все задачи"""
    tasks.clear()
    save_tasks(tasks)
    return redirect('/')

@app.route('/complete-all')
def complete_all():
    """Отмечает ВСЕ задачи как выполненные (done = True)"""
    for task in tasks:
        task['done'] = True
    save_tasks(tasks)
    return redirect('/')

@app.route('/uncomplete-all')
def uncomplete_all():
    """Отмечает ВСЕ задачи как НЕвыполненные (done = False)"""
    for task in tasks:
        task['done'] = False
    save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)