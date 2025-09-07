from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
import psycopg
import os
from psycopg.rows import dict_row
from sql_q import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfffdsfdlsdmdss'

url = 'postgres://kostya:2005@localhost:5432/flkurs'

categories = [{'name': 'Палатки', 'url': 'palatkli'},
              {'name': 'Рыбалка', 'url': 'rybalka'},
              {'name': 'Альпинизм', 'url': 'alpinism'}]


@app.route('/')
def index():
    return render_template('index.html', title='Главная', products =get_products() )


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or username != session['userLogged']:
        abort(401)
    return f"Пользователь {username}"


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', categories=categories)


@app.route('/login', methods = ['POST','GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'kostya' and request.form['psw'] == '1':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title='Авторизация', categories=categories)

def get_products():
    with psycopg.connect(url) as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(GET_PRODUCTS)
            res = cursor.fetchall()
            return res


if __name__ == '__main__':
    app.run(debug=True)
    "C:\Users\azavc\PycharmProjects\kursflaska"