from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# --- НАСТРОЙКА БАЗЫ ДАННЫХ ---
# Указываем, что БД будет храниться в файле app.db в папке project
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализируем БД и миграции
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- МОДЕЛЬ NOTES (Пункт 01 и 05) ---
class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) # Заголовок
    text = db.Column(db.Text, nullable=False)         # Текст
    # Пункт 05: Добавляем колонку "Подзаголовок" (пока делаем её необязательной)
    subtitle = db.Column(db.String(200), nullable=True) 

# --- ДАННЫЕ ДЛЯ СТРАНИЦ ---
menu = [
    {"name": "Главная", "url": "/"},
    {"name": "Обо мне", "url": "/about"},
    {"name": "Дневник", "url": "/notes"}
]

themes = [
    {"id": 1, "name": "Основы HTML"},
    {"id": 2, "name": "Стилизация CSS"},
    {"id": 3, "name": "Шаблонизатор Jinja2"}
]

# --- МАРШРУТЫ ---
@app.route('/')
def index():
    return render_template('index.html', page_title="Главная", menu=menu)

@app.route('/about')
def about():
    return render_template('about.html', page_title="Обо мне", menu=menu)

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        
        # Пункт 03: Обработка данных и загрузка в БД
        if title and text:
            new_note = Notes(title=title, text=text)
            db.session.add(new_note) # Добавляем в сессию
            db.session.commit()      # Сохраняем в БД
            
        # После добавления перенаправляем на ту же страницу, чтобы избежать дублирования при обновлении
        return redirect(url_for('notes'))
    
    # Пункт 04: Выгрузка данных из БД
    all_notes = Notes.query.all() # Достаем все записи из таблицы
    
    return render_template('notes.html', page_title="Дневник", menu=menu, notes=all_notes, themes=themes)


if __name__ == '__main__':
    app.run(debug=True)