from flask import Flask, render_template, request, redirect, session
from database import init_db, get_all_messages, add_message, delete_message, delete_all_messages, get_message_count, check_user
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = 'секретный_ключ_для_гостевой_книги_12345'

MONTHS = {
    '01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля',
    '05': 'мая', '06': 'июня', '07': 'июля', '08': 'августа',
    '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'
}

def format_date_ru(date_str):
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return f"{dt.day} {MONTHS[dt.strftime('%m')]} {dt.year}"
    except:
        return date_str

init_db()
today_str = date.today().isoformat()

@app.route('/')
def index():
    messages = get_all_messages(sort_order='DESC')
    for msg in messages:
        msg['date_ru'] = format_date_ru(msg['created_at'])
    
    total_count = get_message_count()
    success = session.pop('success', None)
    error = session.pop('error', None)
    
    return render_template('index.html',
                         messages=messages,
                         total_count=total_count,
                         today=today_str,
                         success=success,
                         error=error,
                         current_sort='newest',
                         logged_in=session.get('logged_in', False),
                         username=session.get('username'))

@app.route('/sort/newest')
def sort_newest():
    messages = get_all_messages(sort_order='DESC')
    for msg in messages:
        msg['date_ru'] = format_date_ru(msg['created_at'])
    
    total_count = get_message_count()
    return render_template('index.html',
                         messages=messages,
                         total_count=total_count,
                         today=today_str,
                         current_sort='newest',
                         logged_in=session.get('logged_in', False),
                         username=session.get('username'))

@app.route('/sort/oldest')
def sort_oldest():
    messages = get_all_messages(sort_order='ASC')
    for msg in messages:
        msg['date_ru'] = format_date_ru(msg['created_at'])
    
    total_count = get_message_count()
    return render_template('index.html',
                         messages=messages,
                         total_count=total_count,
                         today=today_str,
                         current_sort='oldest',
                         logged_in=session.get('logged_in', False),
                         username=session.get('username'))

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()
    
    if not name or not message:
        session['error'] = 'Заполните все поля!'
        return redirect('/')
    
    add_message(name, message)
    session['success'] = 'Сообщение добавлено!'
    return redirect('/')

@app.route('/delete/<int:message_id>')
def delete(message_id):
    """Удаляет сообщение — только для авторизованных"""
    if not session.get('logged_in'):
        session['error'] = 'Для удаления сообщений необходимо войти!'
        return redirect('/login')
    
    delete_message(message_id)
    session['success'] = 'Сообщение удалено!'
    return redirect('/')

@app.route('/delete-all')
def delete_all_page():
    """Страница подтверждения удаления всех сообщений"""
    if not session.get('logged_in'):
        session['error'] = 'Для удаления всех сообщений необходимо войти!'
        return redirect('/login')
    
    total_count = get_message_count()
    return render_template('delete_all.html', total_count=total_count)

@app.route('/delete-all-confirm', methods=['POST'])
def delete_all_confirm():
    """Удаляет все сообщения"""
    if not session.get('logged_in'):
        return redirect('/login')
    
    delete_all_messages()
    session['success'] = 'Все сообщения удалены!'
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа в приложение"""
    error = None
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if check_user(username, password):
            session['logged_in'] = True
            session['username'] = username
            session['success'] = f'Добро пожаловать, {username}!'
            return redirect('/')
        else:
            error = 'Неверный логин или пароль'
    
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """Выход из приложения"""
    session.pop('logged_in', None)
    session.pop('username', None)
    session['success'] = 'Вы вышли из системы'
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
