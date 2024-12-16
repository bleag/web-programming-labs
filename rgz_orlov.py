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
        db_path = path.join(dir_path, "database.db")
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
  
    if data['username'] == '':
        return {'username': 'Заполните никнэйм'}, 400
    if data['password'] == '':
        return {'password': 'Заполните пароль'}, 400
    password_hash = generate_password_hash(data['password'])
    try:
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id",
                        (data['username'], password_hash))
        else:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                        (data['username'], password_hash))
    except Exception as e:
        return{'exception': str(e)}, 400

    new_user_id = cur.fetchone()['id'] 
    if current_app.config['DB_TYPE'] == 'postgres':
        pass 
    else:
        cur.lastrowid
    db_close(conn, cur)
    return {"index": new_user_id}, 201


@rgz_orlov.route('/rgz/rest-api/users/login', methods=['POST'])
def login_user():
    data = request.get_json()

    # Проверяем наличие введенных данных
    if data['username'] == '':
        return {'username': 'Введите никнэйм'}, 400
    if data['password'] == '':
        return {'password': 'Введите пароль'}, 400

    try:
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id, username, password FROM users WHERE username = %s", (data['username'],))
        else:
            cur.execute("SELECT id, username, password FROM users WHERE username = ?", (data['username'],))

        user = cur.fetchone()
        if not user:
            return {'username': 'Пользователь не найден'}, 400

        # Проверка пароля
        if not check_password_hash(user['password'], data['password']):
            return {'password': 'Неверный пароль'}, 400

        # Успешный вход
        session['user_id'] = user['id'] 
        session['username'] = user['username']
        db_close(conn, cur)
        return {}, 200
    except Exception as e:
        return {'exception': str(e)}, 400
    
@rgz_orlov.route('/main')
def rgz_orlov_main_page():
    if 'user_id' not in session:
        return redirect('/rgz') 
    else:
        user_id = session['user_id']
        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM profiles WHERE user_id = %s", (user_id,))
        else:
            cur.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,))
        profile = cur.fetchone()
        db_close(conn, cur)
        if profile:
            profile['photo_path'] = str(profile['photo_path']).replace('\\', '/')
        else:
            return render_template ('rgz/main.html')
        return render_template('rgz/main.html', username=session['username'], profile=profile)
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
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                """
                UPDATE profiles
                SET name = %s, age = %s, gender = %s, looking_for = %s, about = %s, photo_path = %s
                WHERE user_id = %s
                """,
                (name, age, gender, looking_for, about, photo_path, user_id),
            )
        else:
            cur.execute(
                """
                UPDATE profiles
                SET name = ?, age = ?, gender = ?, looking_for = ?, about = ?, photo_path = ?
                WHERE user_id = ?
                """,
                (name, age, gender, looking_for, about, photo_path, user_id),
            )
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

        # Очистка сессии после удаления профиля
        session.clear()
        return {'message': 'Аккаунт успешно удален'}, 200
    except Exception as e:
        return {'message': str(e)}, 500



@rgz_orlov.route('/rgz/rest-api/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/rgz')