from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div_form')
def div_form():
    return render_template('lab4/div_form.html')

@lab4.route('/lab4/add_form')
def add_form():
    return render_template('lab4/add_form.html')

@lab4.route('/lab4/sub_form')
def sub_form():
    return render_template('lab4/sub_form.html')

@lab4.route('/lab4/mul_form')
def mul_form():
    return render_template('lab4/mul_form.html')

@lab4.route('/lab4/pow_form')
def pow_form():
    return render_template('lab4/pow_form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    # Получаем данные из формы
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    # Проверяем, заполнены ли оба поля
    if x1 == "" or x2 == "":
        return render_template('lab4/div.html', x1=x1, x2=x2, result=None, error='Оба поля должны быть заполнены')

    try:
        # Преобразуем ввод в целые числа
        x1 = int(x1)
        x2 = int(x2)
        
        # Выполняем деление
        result = x1 / x2

    except ValueError:
        # Обработка ошибки, если ввод не целое число
        return render_template('lab4/div.html', x1=x1, x2=x2, result=None, error='Ввод должен быть целыми числами')
    
    except ZeroDivisionError:
        # Обработка деления на ноль
        return render_template('lab4/div.html', x1=x1, x2=x2, result=None, error='Деление на ноль невозможно')

    # Возвращаем результат, если всё прошло успешно
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result, error=None)
    
@lab4.route('/lab4/add', methods=['POST'])
def add():
    x1 = request.form.get('x1') or '0'  # Пустое поле трактуется как 0
    x2 = request.form.get('x2') or '0'

    try:
        result = int(x1) + int(x2)
    except ValueError:
        return render_template('lab4/add.html', x1=x1, x2=x2, result=None, error='Ввод должен быть целыми числами')

    return render_template('lab4/add.html', x1=x1, x2=x2, result=result, error=None)


# --- Вычитание ---
@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == "" or x2 == "":
        return render_template('lab4/sub.html', x1=x1, x2=x2, result=None, error='Оба поля должны быть заполнены')

    try:
        result = int(x1) - int(x2)
    except ValueError:
        return render_template('lab4/sub.html', x1=x1, x2=x2, result=None, error='Ввод должен быть целыми числами')

    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result, error=None)


# --- Умножение ---
@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1') or '1'  # Пустое поле трактуется как 1
    x2 = request.form.get('x2') or '1'

    try:
        result = int(x1) * int(x2)
    except ValueError:
        return render_template('lab4/mul.html', x1=x1, x2=x2, result=None, error='Ввод должен быть целыми числами')

    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result, error=None)


# --- Возведение в степень ---
@lab4.route('/lab4/pow', methods=['POST'])
def pow_op():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == "" or x2 == "":
        return render_template('lab4/pow.html', x1=x1, x2=x2, result=None, error='Оба поля должны быть заполнены')

    try:
        x1 = int(x1)
        x2 = int(x2)

        if x1 == 0 and x2 == 0:
            raise ValueError("0  0 не определено")

        result = x1 ** x2
    except ValueError as e:
        return render_template('lab4/pow.html', x1=x1, x2=x2, result=None, error=str(e))

    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result, error=None)



tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count

    if request.method == 'POST':
        operation = request.form.get('operation')

        # Увеличиваем или уменьшаем счётчик с проверками
        if operation == 'cut' and tree_count > 0:
            tree_count -= 1
        elif operation == 'plant' and tree_count < 10:
            tree_count += 1

        # POST/Redirect/GET для предотвращения повторной отправки данных
        return redirect('/lab4/tree')
    return render_template('lab4/tree.html', tree_count=tree_count)

users = [
    {'login': 'alex', 'password': '123'}, 
    {'login': 'bob', 'password': '555'}, 
    {'login': 'andrey', 'password': '111'},
    {'login': 'egor', 'password': '999'}
]

@lab4.route('/lab4/login',methods =['GET','POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
        else:
            authorized = False
            login = ''
        return render_template ('lab4/login.html', authorized= authorized,login=login)
    
    login = request.form.get('login')
    password = request.form.get('password')

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect ('/lab4/login')
    
    error = 'Неверный логин и/или пароль'
    return render_template ('lab4/login.html', error=error, authorized = False)


@lab4.route('/lab4/logout', methods= ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')