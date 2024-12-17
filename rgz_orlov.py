from flask import Blueprint,  render_template, request, redirect, jsonify, session, current_app
from os import path
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
rgz_orlov = Blueprint('rgz_orlov', __name__)


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='orlov_andrey_base',
            user='orlov_andrey_knowledge_base',
            password='123',
            options="-c client_encoding=UTF8"
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database1.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@rgz_orlov.route('/rgz')
def rgz():
    return render_template('rgz/login.html')


@rgz_orlov.route('/rgz/rest-api/users/registration', methods=['POST'])
def add_user():
    data = request.get_json()
  
    # Проверка на пустые поля
    if not data.get('username'):
        return {'username': 'Заполните никнэйм'}, 400
    if not data.get('password'):
        return {'password': 'Заполните пароль'}, 400
    
    password_hash = generate_password_hash(data['password'])
    try:
        conn, cur = db_connect()

        if current_app.config['DB_TYPE'] == 'postgres':
            # Вставка и возврат ID новой записи
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id",
                (data['username'], password_hash)
            )
            new_user_id = cur.fetchone()['id']
        else:
            # Вставка в SQLite
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (data['username'], password_hash)
            )
            new_user_id = cur.lastrowid  
        
        db_close(conn, cur)
        return {"index": new_user_id}, 201

    except Exception as e:
        db_close(conn, cur)
        return {'exception': str(e)}, 400


@rgz_orlov.route('/rgz/rest-api/users/login', methods=['POST'])
def login_user():
    data = request.get_json()

    # Проверяем наличие введенных данных
    if not data.get('username'):
        return {'username': 'Введите никнэйм'}, 400
    if not data.get('password'):
        return {'password': 'Введите пароль'}, 400

    try:
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id, username, password FROM users WHERE username = %s", (data['username'],))
            user = cur.fetchone()  # Возвращает словарь через RealDictCursor
        else:
            cur.execute("SELECT id, username, password FROM users WHERE username = ?", (data['username'],))
            user = cur.fetchone()  # Возвращает sqlite3.Row

        if not user:
            db_close(conn, cur)
            return {'username': 'Пользователь не найден'}, 400

        # Получаем данные пользователя в виде словаря
        user_id = user['id'] if current_app.config['DB_TYPE'] == 'postgres' else user['id']
        username = user['username'] if current_app.config['DB_TYPE'] == 'postgres' else user['username']
        password_hash = user['password'] if current_app.config['DB_TYPE'] == 'postgres' else user['password']

        # Проверка пароля
        if not check_password_hash(password_hash, data['password']):
            db_close(conn, cur)
            return {'password': 'Неверный пароль'}, 400

        # Успешный вход
        session['user_id'] = user_id
        session['username'] = username
        db_close(conn, cur)
        return {}, 200

    except Exception as e:
        db_close(conn, cur)
        return {'exception': str(e)}, 400
    
@rgz_orlov.route('/main')
def rgz_orlov_main_page():
    if 'user_id' not in session:
        return redirect('/rgz')  # Если пользователь не авторизован, перенаправляем на страницу логина
    
    try:
        user_id = session['user_id']
        conn, cur = db_connect()

        # Выполняем запрос к базе данных
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM profiles WHERE user_id = %s", (user_id,))
        else:
            cur.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,))
        
        profile = cur.fetchone()

        # Закрываем соединение
        db_close(conn, cur)

        # Проверяем, найден ли профиль
        if profile:
            # Приведение пути к фото в корректный формат
            photo_path = profile['photo_path'] if current_app.config['DB_TYPE'] == 'postgres' else profile['photo_path']
            profile = dict(profile)  # Преобразуем sqlite3.Row в словарь для совместимости
            if photo_path:
                profile['photo_path'] = str(photo_path).replace('\\', '/')
        else:
            return render_template('rgz/main.html')  # Если профиль не найден, загружаем пустую страницу

        return render_template('rgz/main.html', username=session['username'], profile=profile)
    
    except Exception as e:
        # Если возникает ошибка, возвращаем сообщение об ошибке
        return {'message': str(e)}, 500

@rgz_orlov.route('/rgz/rest-api/profiles', methods=['POST'])
def add_profile():
    if 'user_id' not in session:
        return {'message': 'Не авторизован'}, 403

    user_id = session['user_id']
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    looking_for = request.form.get('looking_for')
    about = request.form.get('about', '')
    photo = request.files.get('photo')

    # Проверка обязательных данных
    if not name or not age or not gender or not looking_for:
        return {'message': 'Заполните все обязательные поля'}, 400

    photo_path = None
    if photo:
        filename = secure_filename(f"user_{user_id}_{photo.filename}")
        save_path = path.join(current_app.config['UPLOAD_FOLDER'], filename)
        photo.save(save_path)
        photo_path = path.join('uploads', filename)

    try:
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                """
                INSERT INTO profiles (user_id, name, age, gender, looking_for, about, photo_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (user_id, name, age, gender, looking_for, about, photo_path),
            )
        else:
            cur.execute(
                """
                INSERT INTO profiles (user_id, name, age, gender, looking_for, about, photo_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, name, age, gender, looking_for, about, photo_path),
            )
        db_close(conn, cur)
        return {}, 201
    except Exception as e:
        return {'message': str(e)}, 500
    
@rgz_orlov.route('/rgz/rest-api/profiles', methods=['PUT'])
def update_profile():
    if 'user_id' not in session:
        return {'message': 'Не авторизован'}, 403

    user_id = session['user_id']
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    looking_for = request.form.get('looking_for')
    about = request.form.get('about', '')
    photo = request.files.get('photo')
    is_hidden = request.form.get('is_hidden') == 'true'

    # Проверка обязательных данных
    if not name or not age or not gender or not looking_for:
        return {'message': 'Заполните все обязательные поля'}, 400

    photo_path = None
    if photo:
        filename = secure_filename(f"user_{user_id}_{photo.filename}")
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        photo.save(save_path)
        photo_path = os.path.join('uploads', filename)

    try:
        conn, cur = db_connect()
        
        # SQL-запрос в зависимости от наличия фото
        if photo_path:
            query_postgres = """
                UPDATE profiles
                SET name = %s, age = %s, gender = %s, looking_for = %s, about = %s, photo_path = %s, is_hidden = %s
                WHERE user_id = %s
            """
            query_sqlite = """
                UPDATE profiles
                SET name = ?, age = ?, gender = ?, looking_for = ?, about = ?, photo_path = ?, is_hidden = ?
                WHERE user_id = ?
            """
            params = (name, age, gender, looking_for, about, photo_path, is_hidden, user_id)
        else:
            query_postgres = """
                UPDATE profiles
                SET name = %s, age = %s, gender = %s, looking_for = %s, about = %s, is_hidden = %s
                WHERE user_id = %s
            """
            query_sqlite = """
                UPDATE profiles
                SET name = ?, age = ?, gender = ?, looking_for = ?, about = ?, is_hidden = ?
                WHERE user_id = ?
            """
            params = (name, age, gender, looking_for, about, is_hidden, user_id)

        # Выполняем SQL-запрос
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(query_postgres, params)
        else:
            cur.execute(query_sqlite, params)

        # Подтверждаем изменения и закрываем соединение
        conn.commit()
        db_close(conn, cur)
        return {'message': 'Профиль успешно обновлен'}, 200
    except Exception as e:
        return {'message': str(e)}, 500

@rgz_orlov.route('/rgz/rest-api/profiles/delete', methods=['DELETE'])
def delete_profile():
    if 'user_id' not in session:
        return {'message': 'Не авторизован'}, 403

    user_id = session['user_id']

    try:
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM profiles WHERE user_id = %s", (user_id,))
        else:
            cur.execute("DELETE FROM profiles WHERE user_id = ?", (user_id,))
        db_close(conn, cur)
        conn.commit()
        # Очистка сессии после удаления профиля
        session.clear()
        return {'message': 'Аккаунт успешно удален'}, 200
    except Exception as e:
        return {'message': str(e)}, 500



@rgz_orlov.route('/rgz/rest-api/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/rgz')


@rgz_orlov.route('/rgz/rest-api/search', methods=['GET'])
def search_profiles():
    if 'user_id' not in session:
        return {'message': 'Не авторизован'}, 403

    # Получаем параметры поиска из запроса
    search_name = request.args.get('name', '').strip()
    search_age = request.args.get('age')
    offset = int(request.args.get('offset', 0))  # Пагинация: начальное смещение
    limit = 3  # Количество записей на страницу

    # Получаем информацию о текущем пользователе для фильтрации по полу
    user_id = session['user_id']
    try:
        conn, cur = db_connect()

        # Получаем пол и пол для поиска текущего пользователя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT gender, looking_for FROM profiles WHERE user_id = %s
            """, (user_id,))
        else:
            cur.execute("""
                SELECT gender, looking_for FROM profiles WHERE user_id = ?
            """, (user_id,))
        
        user_profile = cur.fetchone()
        if not user_profile:
            db_close(conn, cur)
            return {'message': 'Профиль пользователя не найден'}, 404
        
        user_gender = user_profile['gender']
        user_looking_for = user_profile['looking_for']

        # Основной SQL-запрос с фильтрами
        if current_app.config['DB_TYPE'] == 'postgres':
            query = """
                SELECT name, age, gender, about, photo_path
                FROM profiles
                WHERE is_hidden = FALSE
                AND gender = %s
                AND looking_for = %s
            """
            params = [user_looking_for, user_gender]

            if search_name:
                query += " AND name ILIKE %s"
                params.append(f"%{search_name}%")

            if search_age:
                query += " AND age = %s"
                params.append(search_age)

            query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])

        else:
            query = """
                SELECT name, age, gender, about, photo_path
                FROM profiles
                WHERE is_hidden = 0
                AND gender = ?
                AND looking_for = ?
            """
            params = [user_looking_for, user_gender]

            if search_name:
                query += " AND name LIKE ?"
                params.append(f"%{search_name}%")

            if search_age:
                query += " AND age = ?"
                params.append(search_age)

            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])

        cur.execute(query, tuple(params))
        results = cur.fetchall()
        db_close(conn, cur)

        return jsonify([dict(row) for row in results]), 200

    except Exception as e:
        return {'message': str(e)}, 500
