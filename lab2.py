from flask import Blueprint, url_for, redirect, render_template, Response, render_template_string, Blueprint, request
lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@lab2.route('/lab2/filters/')
def filters():
    phrase = '0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных... '
    return render_template('filters.html', phrase = phrase)

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a,b):
    first = a
    second = b
    return render_template('calc.html', first = first, second = second)

@lab2.route('/lab2/calc/')
def redcalc():
    return redirect("/lab2/calc/1/1")

@lab2.route('/lab2/calc/<int:a>')
def redcalccc(a):
    return redirect(f"/lab2/calc/{a}/1")


# Список книг с указанием автора, названия, жанра и количества страниц
books = [
    {"title": "Человек в поисках смысла", "author": "Виктор Франкл", "genre": "Психология", "pages": 224},
    {"title": "Психология влияния", "author": "Роберт Чалдини", "genre": "Социальная психология", "pages": 384},
    {"title": "Думай медленно... решай быстро", "author": "Даниэль Канеман", "genre": "Когнитивная психология", "pages": 704},
    {"title": "Игры, в которые играют люди", "author": "Эрик Берн", "genre": "Психология", "pages": 544},
    {"title": "Эмоциональный интеллект", "author": "Дэниел Гоулман", "genre": "Психология", "pages": 496},
    {"title": "Тревожные люди", "author": "Фредрик Бакман", "genre": "Социальная психология", "pages": 416},
    {"title": "Сила привычки", "author": "Чарльз Дахигг", "genre": "Психология", "pages": 432},
    {"title": "Самообман", "author": "Эдгар Шейн", "genre": "Психология личности", "pages": 320},
    {"title": "Психология зависимости", "author": "Говард Шаффер", "genre": "Психология", "pages": 384},
    {"title": "Мозг и душа", "author": "Валерий Суворов", "genre": "Нейропсихология", "pages": 256}
]
# Обработчик для отображения списка книг
@lab2.route('/lab2/books/')
def book_list():
    return render_template('books.html', books=books)



berries = [
    {"name": "Клубника", "description": "Сладкая и сочная летняя ягода.", "image": "/static/k.webp"},
    {"name": "Малина", "description": "Ягода с нежным ароматом и вкусом.", "image": "/static/ma.webp"},
    {"name": "Голубика", "description": "Темная ягода с насыщенным вкусом.", "image": "/static/g.jpg"},
    {"name": "Ежевика", "description": "Ягода с насыщенным сладким вкусом.", "image": "/static/e.webp"},
    {"name": "Морошка", "description": "Ягода с кисловатым вкусом", "image": "/static/mo.webp"}
]

@lab2.route('/lab2/berries/')
def show_berries():
    return render_template('berries.html', berries=berries)

flower_list = [
    {'name': 'роза', 'price': 300},
    {'name': 'тюльпан', 'price': 310},
    {'name': 'незабудка', 'price': 320},
    {'name': 'ромашка', 'price': 300},
    {'name': 'георгин', 'price': 300},
    {'name': 'гладиолус', 'price': 310}
]

# Обработчик для отображения списка всех цветов
@lab2.route('/lab2/flowers/')
def list_flowers():
    return render_template('flower_list.html', flowers=flower_list)

# Обработчик для добавления нового цветка
@lab2.route('/lab2/add_flower/', methods=['GET'])
def add_flower():
    name = request.args.get('name')
    price = request.args.get('price')
    if name and price:
        flower_list.lab2end({'name': name, 'price': int(price)})
    return redirect(url_for('list_flowers'))

# Обработчик для удаления цветка
@lab2.route('/lab2/del_flower/<int:flower_id>')
def delete_flower(flower_id):
    if 0 <= flower_id < len(flower_list):
        del flower_list[flower_id]
        return redirect(url_for('list_flowers'))
    return  render_template ("404.html"), 404

# Обработчик для очистки всех цветов
@lab2.route('/lab2/clear_flowers/')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('list_flowers'))