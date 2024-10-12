from flask import Blueprint, url_for, redirect, render_template, Response, render_template_string, Blueprint
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1/web")
def web():
    return """<!doctype html> 
        <html> 
                <body> 
                        <h1>web-сервер на flask</h1> 
                        <a href="/lab1/author">author</a>
                </body> 
          </html>"""


@lab1.route("/lab1/author")
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


@lab1.route('/lab1/oak')
def oak():
    path = url_for("static", filename="lab1/oak.jpg")
    css_path = url_for("static", filename="lab1/lab1.css")
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

@lab1.route('/lab1/counter')
def counter():
    global count
    count +=1
    reset_url = url_for('lab1.reset_counter')
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <a href="''' + reset_url + '''">Сбросить счётчик</a>
    </body>
</html>'''    


@lab1.route('/lab1/reset_counter')
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


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
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


@lab1.route('/lab1')
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


@lab1.route('/lab1/about')
def about():
    path = url_for("static", filename="lab1/river.jpg")
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