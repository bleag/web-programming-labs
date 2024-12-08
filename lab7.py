from flask import Blueprint, render_template, request, session,redirect, current_app,abort, make_response,jsonify

lab7 = Blueprint('lab7', __name__)


@lab7.route("/lab7/")
def main():
    return render_template('lab7/index.html')

films = [
    {

        "title": "Holop2",
        "title_ru": "Холоп2",
        "year": 2023,
        "descriprion":"Гриша, бывший мажор, побывавший холопом и ставший человеком, \
        после путешествия в «прошлое» чутко реагирует \
        на любую несправедливость. И, конечно, не может пройти мимо беспредела, который творит наглая и \
        избалованная Катя. Ничего удивительного, что вскоре мажорка обнаруживает себя в другом времени."

    },


     {

        "title": "cheburashka",
        "title_ru": "Чебурашка",
        "year": 2022,
        "descriprion":"Иногда, чтобы вернуть солнце и улыбки в мир взрослых, \
        нужен один маленький ушастый герой. Мохнатого непоседливого зверька из далекой \
        апельсиновой страны ждут удивительные приключения в тихом приморском городке, \
        где ему предстоит найти себе имя, друзей и дом. Помогать — и мешать! — \
        ему в этом будут нелюдимый старик-садовник, странная тетя-модница \
        и ее капризная внучка, мальчик, который никак не …"

    },

     {

        "title": "The last frontier",
        "title_ru": "Последний рубеж",
        "year": 2013,
        "descriprion":"Деревенская мафия открывает охоту за бывшим агентом управления по борьбе с наркотиками. \
        Типичный фильм со Джейсоном Стэйтемом, наполненный перестрелками и рукопашными схватками.\
          Джеймс Франко сыграл харизматичного антагониста по прозвищу Аллегатор. \
          Сценарий к картине написал мэтр западных боевиков Сильвестр Сталлоне."

    },

     {

        "title": "The adventures of paddington 2",
        "title_ru": "Приключение паддингтона 2",
        "year": 2017,
        "descriprion":"Продолжение истории о полюбившемся всем медвежонке Паддингтоне. На этот\
          раз герой отправился на поиски воришки, укравшего уникальную книгу, которую \
          Паддингтон собирался подарить своей тетушке. В остальном все по-прежнему: \
          красивая анимация, шутки и не слишком назидательные разговоры о добре и зле."

    },


     {

        "title": "Ice",
        "title_ru": "Лед",
        "year": 2018,
        "descriprion":"Романтическая история фигуристки Нади, которой хоккеист Саша помогает \
        вернуться в спорт, — это еще и мюзикл. Герои здесь регулярно поют, причем шлягеры \
        разных лет, из репертуара Земфиры, Ивана Дорна и группы 5’Nizza. \
        В роли Надиной матери — актриса Ксения Раппорт, мама актрисы Аглаи Тарасовой в реальной жизни."

    },
]


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return films [id]


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def gel_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    del films[id]
    return '',204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    film = request.get_json()
    if film['description'] == '':
        return {'description': 'Заполните описание'}, 400
    films[id] = film
    return films[id]


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    if film['description'] == '':
        return {'description': 'Заполните описание'}, 400
    new_id = len(films)
    film["id"] = new_id 
    films.append(film)
    return film
