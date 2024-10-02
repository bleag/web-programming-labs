from flask import Flask, url_for, redirect, render_template, Response, render_template_string
app = Flask(__name__)


@app.route("/")
def slesh():
     return redirect('/lab1/menu', code=302)


@app.route("/index")
def index():
     return redirect('/lab1/menu', code=302)


@app.route("/lab1/web")
def web():
    return """<!doctype html> 
        <html> 
                <body> 
                        <h1>web-сервер на flask</h1> 
                        <a href="/lab1/author">author</a>
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
                <a href= "/lab1/web">web</a>
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
    return redirect("/lab1/author")

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
    return  render_template ("404.html"), 404

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
            &copy; Орлов Андрей, ФБИ-21, 3 курс, 2024
        </footer>
    </body>
</html>'''

@app.route('/lab1')
def lab():
    return '''
<!doctype html>
<html>
    <head>
        <title>Орлов Андрей Викторович, Лабораторная 1</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: lightpurple;
                color: #333;
                line-height: 1.6;
                margin: 20px;
                font-size: 15px;
            }
            h1 {
                text-align: center;
                color: blue;
                margin-bottom: 10px;
        
        </style>
    </head>

    <body>
        <header>
            Лабораторная работа 1
        </header>

        <h1>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности. <br>        
            
            <a href="/">Меню</a>
        </h1>
        <h2>Реализованные роуты</h2>
        <div>
            <ol>
            <li><a href="/lab1/oak">Дуб</a></li>
            <li><a href="/lab1/web">веб-сервер на фласк</a></li>
            <li><a href="/lab1/author">студент-группа - факультет</a></li>
            <li><a href="/lab1/counter">Счетчик</a></li>
            <li><a href="/lab1/created">201 код</a></li>
            <li><a href="404"> ошибка 404</a></li>
            <li><a href="400">Ошибка 400</a></li>
            <li><a href="401">Ошибка 401</a></li>
            <li><a href="402">Ошибка 402</a></li>
            <li><a href="403">Ошибка 403</a></li>
            <li><a href="405">Ошибка 405</a></li>
            <li><a href="418">Ошибка 418</a></li>
            <li><a href="/about"> заголовки</a></li>
            <li><a href ="/error">ошибка 500</a></li>
            <li><a href="/lab1/web1"> веб-сервер на flask</a><li>
            </ol>
        <div>
    </body>

        <footer>
            &copy; Орлов Андрей, ФБИ-21, 3 курс, 2024
        </footer>
    </body> 
</html>
'''


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

@app.route('/about')
def about():
    path = url_for("static", filename="river.jpg")
    html_content = '''
    <!doctype html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Осень</title>
         <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f9f9f9;
                color: #333;
                line-height: 1.6;
                margin: 20px;
            }
            h1 {
                text-align: center;
                color: #c65d3b;
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            p {
                padding: 10px 20px;
                border-left: 3px solid #c65d3b;
                background: #fff;
                margin: 20px 0;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
        </style>
    </head>
    
    <body>
            <h1>Река</h1>
            <p>
               В далекой уютной деревне, среди заливных полей и высоких холмов, тянется одна из красивейших рек. 
               Ее прозрачная вода и благоухающие берега притягивают к себе множество путешественников и любителей природы. Здесь, где время замирает, 
               каждый камень и каждое дерево имеют свою историю, свою тайну, которые манят гостей раскрывать незабываемые загадки природы.
            </p>
           <p>
                В этих краях ты находишься в полном единении с природой. Шум воды, пение птиц и шелест листвы наполняют сердце и дарят умиротворение. Здесь можно встретить оленей и зайцев, которые бесстрашно прогуливаются 
                по полям и лесам. Каждый шаг вдоль реки открывает все новые и новые красоты, заставляя погрузиться в завораживающую симфонию природы.
            </p>
            <p>
                В моменты, когда солнце падает за горизонт, а небосвод окрашивается в огненные оттенки, река приобретает особую магию. 
                Ее рассветы и закаты — подарок для каждого, кто позволяет себе остановиться и насладиться этой красотой. 
                Здесь, среди деревьев и воды, ты найдешь покой и вдохновение, открывая новые грани своего внутреннего мира.
            </p>
            <img src="''' + path + '''">
    </body>
    </html>'''
   
    response = Response(render_template_string(html_content))
    response.headers['Content-Language'] = 'ru'
    response.headers['Content-Type'] = 'text/html'
    response.headers['Content-Length'] = response.calculate_content_length()
   
    return response

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a1():
    return 'со слешем'

flower_list = ['роза', 'тюльпан', 'незабудка' , 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return '''
        <!doctype html>
        <html>
            <body>
            <h1>Такого изящного цветочка нету</h1>
            <p><a href="/lab2/flowers/">Вернуться ко всем цветам</a></p>
            </body>
        </html>
        ''', 404
    else:
        return f'''
        <!doctype html>
        <html>
            <body>
            <h1>Прекрасный цветочек</h1>
            <p>Название: {flower_list[flower_id]}</p>
            <p><a href="/lab2/flowers/">Вернуться ко всем цветам</a></p>
            </body>
        </html>
        '''
    
@app.route('/lab2/add_flower/')
@app.route('/lab2/add_flower/<name>')
def add_flower(name=None):
    if not name:  # Если имя не указано
        return "вы не задали имя цветка", 400
    
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
     <p><a href="/lab2/flowers/">Перейти ко всем цветам</a></p>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name, number, groupe, course='Орлов Андрей', 2, 'ФБИ-21', '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95}, 
        {'name': 'манго', 'price': 321},
    ]
    return render_template('example.html', name=name, number=number, groupe=groupe, course=course, fruits=fruits)



@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = '0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных... '
    return render_template('filters.html', phrase = phrase)

@app.route('/lab2/flowers/')
def list_flowers():
    if not flower_list:
        return '''
        <!doctype html>
        <html>
            <body>
            <h1>Список цветов пуст</h1>
            <p><a href="/lab2/add_flower/">Добавить новый цветок</a></p>
            </body>
        </html>
        '''
    return f'''
    <!doctype html>
    <html>
        <body>
        <h1>Все цветы</h1>
        <p>Всего цветов: {len(flower_list)}</p>
        <ul>
            {''.join(f'<li>{i + 1}. {flower}</li>' for i, flower in enumerate(flower_list))}
        </ul>
        <p><a href="/lab2/add_flower/">Добавить новый цветок</a></p>
        <p><a href="/lab2/clear_flowers/">Очистить все цветы</a></p>
        </body>
    </html>
    '''
@app.route('/lab2/clear_flowers/')
def clear_flowers():
    flower_list.clear()
    return '''
    <!doctype html>
    <html>
        <body>
        <h1>Список цветов очищен</h1>
        <p><a href="/lab2/flowers/">Перейти ко всем цветам</a></p>
        </body>
    </html>
    '''