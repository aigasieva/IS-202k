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
    return render_template('index.html', tasks=tasks, filter_type='all', search_query='')

# ==================== ПОИСК ====================
@app.route('/search')
def search():
    """Поиск задач по тексту (без учёта регистра)"""
    query = request.args.get('q', '').strip().lower()
    if query:
        filtered_tasks = [task for task in tasks if query in task['text'].lower()]
    else:
        filtered_tasks = tasks
    return render_template('index.html', tasks=filtered_tasks, filter_type='search', search_query=query)

# ==================== СОРТИРОВКИ ====================
@app.route('/sort/date')
def sort_by_date():
    """Сортировка по дате (новые задачи сверху)"""
    sorted_tasks = sorted(tasks, key=lambda t: t.get('date', ''), reverse=True)
    return render_template('index.html', tasks=sorted_tasks, filter_type='sort_date', search_query='')

@app.route('/sort/status')
def sort_by_status():
    """Сортировка по статусу (сначала активные, потом выполненные)"""
    sorted_tasks = sorted(tasks, key=lambda t: t.get('done', False))
    return render_template('index.html', tasks=sorted_tasks, filter_type='sort_status', search_query='')

@app.route('/sort/priority')
def sort_by_priority():
    """Сортировка по приоритету (высокий → средний → низкий)"""
    priority_order = {'высокий': 1, 'средний': 2, 'низкий': 3}
    sorted_tasks = sorted(
        tasks,
        key=lambda t: priority_order.get(t.get('priority', 'средний'), 2)
    )
    return render_template('index.html', tasks=sorted_tasks, filter_type='sort_priority', search_query='')

@app.route('/sort/alpha')
def sort_by_alpha():
    """Сортировка по алфавиту (А → Я)"""
    sorted_tasks = sorted(tasks, key=lambda t: t.get('text', '').lower())
    return render_template('index.html', tasks=sorted_tasks, filter_type='sort_alpha', search_query='')

# ==================== ОСНОВНЫЕ МАРШРУТЫ ====================
@app.route('/active')
def show_active():
    """Показывает только НЕвыполненные задачи"""
    active_tasks = [task for task in tasks if not task.get('done', False)]
    return render_template('index.html', tasks=active_tasks, filter_type='active', search_query='')

@app.route('/completed')
def show_completed():
    """Показывает только выполненные задачи"""
    completed_tasks = [task for task in tasks if task.get('done', False)]
    return render_template('index.html', tasks=completed_tasks, filter_type='completed', search_query='')

@app.route('/add', methods=['POST'])
def add_task():
    """Добавляет новую задачу"""
    new_task_text = request.form.get('task', '').strip()
    priority = request.form.get('priority', 'средний')
    
    if new_task_text:
        new_task = {
            'text': new_task_text,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'done': False,
            'priority': priority
        }
        tasks.append(new_task)
        save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Удаляет задачу"""
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect('/')

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    """Переключает статус выполнения"""
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = not tasks[task_id].get('done', False)
        save_tasks(tasks)
    return redirect('/')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """Редактирует задачу"""
    if task_id < 0 or task_id >= len(tasks):
        return "Задача не найдена", 404
    
    task = tasks[task_id]
    
    if request.method == 'POST':
        new_text = request.form.get('task', '').strip()
        new_priority = request.form.get('priority', 'средний')
        old_text = task.get('text', '')
        old_priority = task.get('priority', 'средний')
        
        if new_text == '':
            return render_template('edit.html', task=task, message="❌ Текст не может быть пустым!")
        
        if new_text == old_text and new_priority == old_priority:
            return render_template('edit.html', task=task, message="ℹ️ Ничего не изменено.")
        
        task['text'] = new_text
        task['priority'] = new_priority
        save_tasks(tasks)
        return redirect('/')
    
    return render_template('edit.html', task=task)

@app.route('/clear')
def clear_all():
    """Очищает все задачи"""
    tasks.clear()
    save_tasks(tasks)
    return redirect('/')

@app.route('/complete-all')
def complete_all():
    """Выполнить все"""
    for task in tasks:
        task['done'] = True
    save_tasks(tasks)
    return redirect('/')

@app.route('/uncomplete-all')
def uncomplete_all():
    """Отменить все"""
    for task in tasks:
        task['done'] = False
    save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)