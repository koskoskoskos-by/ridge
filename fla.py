from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
import psycopg
import os
from psycopg.rows import dict_row
from sql_q import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfffdsfdlsdmdss'

url = 'postgres://kostya:2005@localhost:5432/flkurs'


@app.route('/')
def index():
    sort_by = request.args.get('sort', 'GET_POPULAR_PRODUCTS')
    products = get_products(sort_by)
    return render_template('index.html', products=products, sort_by=sort_by)


@app.route('/remove-from-cart', methods=["POST"])
def remove_product():
    prod_id = request.form.get('id')
    if prod_id in session['cart']:
        session['cart'].remove(prod_id)
        change_quantity(prod_id, -1)
        session.modified = True
        if len(session['cart']) == 0 :
            return redirect(url_for('index'))
        else:
            return redirect(url_for('cart'))
    else:
        flash("Товар не найден в корзине")
        return redirect(url_for('cart'))


@app.route('/add-to-cart', methods=["POST"])
def buy_product():
    prod_id = request.form.get('id')
    if prod_id is not None:
        if 'cart' not in session:
            session['cart'] = []
        session['cart'].append(prod_id)
        if None in session['cart']:
            session['cart'].remove(None)
        change_quantity(prod_id, 1)
        session.modified = True
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cart = session['cart']
    return render_template('cart.html', cart=get_cart(cart))


def get_cart(cart):
    with psycopg.connect(url) as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            placeholders = ','.join(['%s'] * len(cart))
            query = f"SELECT * FROM products WHERE id IN ({placeholders})"
            cursor.execute(query, tuple(cart))
            res = cursor.fetchall()
            if res:
                product_name = res[-1]['name']
                flash(f"{product_name} добавлен в корзину")
            return res


def get_products(sort_by):
    with psycopg.connect(url) as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            if sort_by == 'GET_POPULAR_PRODUCTS':
                cursor.execute(GET_POPULAR_PRODUCTS)
            elif sort_by == 'GET_CHEAP_PRODUCTS':
                cursor.execute(GET_CHEAP_PRODUCTS)
            elif sort_by == 'GET_EXPENSIVE_PRODUCTS':
                cursor.execute(GET_EXPENSIVE_PRODUCTS)
            res = cursor.fetchall()
            return res


def change_quantity(id, value):
    with psycopg.connect(url) as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                "UPDATE products SET stock_quantity = stock_quantity - %s WHERE id = %s",
                (value, int(id))
            )
        connection.commit()
        return


if __name__ == '__main__':
    app.run(debug=True)