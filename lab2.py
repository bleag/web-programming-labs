from flask import Flask, url_for, redirect, render_template, Response, render_template_string
lab2 = Flask(__name__)



@lab2.route('/lab2/a')
def a():
    return 'без слэша'

@lab2.route('/lab2/a/')
def a1():
    return 'со слешем'

flower_list = ['роза', 'тюльпан', 'незабудка' , 'ромашка']

@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "такого изящного цветочка нету" , 404
    else:
        return "прекрасный цветочек:   " + flower_list[flower_id]
    
@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный спискок: {flower_list}</p>
</html>
'''

@lab2.route('/lab2/example')
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



@lab2.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@lab2.route('/lab2/filters')
def filters():
    phrase = '0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных... '
    return render_template('filters.html', phrase = phrase)