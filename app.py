from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.route("/lab1/web")
def web():
    return """<!doctype html> 
        <html> 
                <body> 
                        <h1>web-сервер на flask</h1> 
                        <a href="/author">author</a>
                </body> 
          </html>"""



@app.route("/lab1/author")
def author():
    name = "Орлов Андрей Викторович"
    group = "ФБИ-21"
    faculty = "FB"

    return """ <!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """ </p>
                <p>Группа: """ + group + """ </p>
                <p>Факультет: """ + faculty + """ </p>
                <a href= "/web">web</a>
            </body>
        </html>"""

@app.route('/lab1/oak')
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <body>
        <h1>Дуб</h1>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
        <img src="''' + path + '''">
    </body>
</html>'''

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count +=1
    reset_url = url_for('reset_counter')
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <a href="''' + reset_url + '''">Сбросить счётчик</a>
    </body>
</html>'''    

@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0  
    return '''
    <!doctype html>
    <html>
        <body>
            <p>Счётчик сброшен!</p>
            <!-- Ссылка обратно на страницу счётчика -->
            <a href="/lab1/counter">Вернуться к счётчику</a>
        </body>
    </html>'''

@app.route("/lab1/info")
def info():
    return redirect("/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''',201  

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

@app.route("/lab1/web1")
def web1():
     return """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
            </body>
        </html>  """ ,200 , {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route("/lab1/menu")
def menu():
    css_path = url_for("static", filename="lab1.css")
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
        <h2><a href="/lab1">Первая лабораторная</a></h2>
        <h2><a href="/lab2">Вторая лабораторная</a></h2>
        <h2><a href="/lab3">Третья лабораторная</a></h2>
        <h2><a href="/lab4">Четвёртая лабораторная</a></h2>
        <h2><a href="/lab5">Пятая лабораторная</a></h2>
        <h2><a href="/lab6">Шестая лабораторная</a></h2>
        <h2><a href="/lab7">Седьмая лабораторная</a></h2>
        <h2><a href="/lab8">Восьмая лабораторная</a></h2>
        <h2><a href="/lab9">Девятая лабораторная</a></h2>

        <footer>
            &copy; Орлов Андрей, ФБИ-21, 3 курс, 2023
        </footer>
    </body>
</html>'''