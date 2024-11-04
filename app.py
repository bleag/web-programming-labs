from flask import Flask, url_for, redirect, render_template, Response, render_template_string, os
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)


@app.route("/")
def slesh():
     return redirect('/menu', code=302)


@app.route("/index")
def index():
     return redirect('/lab1/menu', code=302)


@app.errorhandler(404)
def not_found(err):
    return  render_template ("404.html"), 404


@app.route("/menu")
def menu():
    css_path = url_for("static", filename="lab1/lab1.css")
    return '''
<!DOCTYPE html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">       
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>
        <ol>
        <li><a href="/lab1">Первая лабораторная</a></li>
        <li><a href="/lab2">Вторая лабораторная</a></li>
        <li><a href="/lab3">Третья лабораторная</a></li>
        <li><a href="/lab4">Четвёртая лабораторная</a></li>
        <li><a href="/lab5">Пятая лабораторная</a></li>
        <li><a href="/lab6">Шестая лабораторная</a></li>
        <li><a href="/lab7">Седьмая лабораторная</a></li>
        <li><a href="/lab8">Восьмая лабораторная</a></li>
        <li><a href="/lab9">Девятая лабораторная</a></li>
        </ol>
        <footer>
            &copy; Орлов Андрей, ФБИ-21, 3 курс, 2024
        </footer>
    </body>
</html>'''


@app.route('/400')
def error_400():
    return Response('Неверный запрос', status=400)

@app.route('/401')
def error_401():
    return Response('Неавторизованный доступ', status=401)

@app.route('/402')
def error_402():
    return Response('Необходима оплата', status=402)

@app.route('/403')
def error_403():
    return Response('Доступ запрещён', status=403)

@app.route('/405')
def error_405():
    return Response('Метод не разрешён', status=405)

@app.route('/418')
def error_418():
    return Response('Я чайник', status=418)


@app.route('/error')
def trigger_error():
    result = 1 / 0
    return str(result)

@app.errorhandler(500)
def internal_server_error(err):
    return render_template('500.html'), 500


