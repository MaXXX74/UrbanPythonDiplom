from flask import Flask, render_template, request, session
from database import DBase

app = Flask(__name__)
app.secret_key = 'hdggrtt465673728kgjj6'

menu = [
    {"label": "Каталог", "link": "/"},
    {"label": "Поиск", "link": "#", "id": "search_button"}
]


@app.route("/page/<int:page>/")
@app.route("/")
def index_page(page=1):
    db = DBase()
    movies_lst, pages = db.get_movies_for_index_page(page=page)
    if len(movies_lst) > 0:
        return render_template("index.html", title="Каталог фильмов", menu=menu,
                           movies=movies_lst, pages=pages)
    else:
        return render_template("nodata.html", title="Нет данных", menu=menu, pages=pages)


@app.route("/search/page/<int:page>/")
@app.route("/search/", methods=['GET', 'POST'])
def search_page(page=1):
    if request.args:
        session["last_request"] = request.args
    
    # if request.form:
    #     session["last_request"] = request.form
    last_request = session.get("last_request", None)

    db = DBase()
    movies_lst, pages = db.get_movies_for_index_page(args=last_request, page=page)
    if len(movies_lst) > 0:
        return render_template("index.html", title="Результат поиска", menu=menu,
                           movies=movies_lst, pages=pages, source="search")
    else:
        return render_template("nodata.html", title="Нет данных", menu=menu,
                           pages=pages, source="search")



@app.route("/movie/<int:id>/")
def movie_page(id: int):
    db = DBase()
    movie = db.get_movie_by_id(id)
    shots = db.get_shots_by_id(id)
    if movie:
        return render_template("movie.html", menu=menu, movie=movie, shots=shots)
    else:
        return render_template("nodata.html", title="Нет данных", menu=menu, pages=(None, None))


if __name__ == "__main__":
    app.run(debug=True)
