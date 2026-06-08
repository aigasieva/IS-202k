from flask import Flask, render_template, request, redirect, session
from database import init_db, get_all_messages, add_message
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'my_secret_key_12345'

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

@app.route('/')
def index():
    messages = get_all_messages()
    for msg in messages:
        msg['date_ru'] = format_date_ru(msg['created_at'])
    
    success = session.pop('success', None)
    error = session.pop('error', None)
    
    return render_template('index.html', 
                         messages=messages, 
                         success=success, 
                         error=error)

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

if __name__ == '__main__':
    app.run(debug=True)
