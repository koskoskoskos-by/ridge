from flask import Flask, render_template, url_for, request, flash, session, redirect
from sql_q import *
from forms import *
from werkzeug.security import check_password_hash,generate_password_hash
from User import *
from flask_login import LoginManager, login_manager, login_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfffdsfdlsdmdss'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

url = 'postgres://postgres:567567@localhost:5432/flkurs'



@login_manager.user_loader
def load_user(id):
    return UserLogin().fromDB(id, db)


@app.route('/')
def index():
    sort_by = request.args.get('sort', 'stock_quantity desc')
    products = db.sort_by(sort_by)
    return render_template('index.html', products=products, sort_by=sort_by)


@app.route('/remove-from-cart', methods=["POST"])
@login_required
def remove_product():
    prod_id = request.form.get('id')
    if prod_id in session['cart']:
        session['cart'].remove(prod_id)
        db.change_quantity(prod_id, -1)
        session.modified = True
        if len(session['cart']) == 0 :
            return redirect(url_for('index'))
        else:
            return redirect(url_for('cart'))
    else:
        flash("Товар не найден в корзине", 'unsuccess')
        return redirect(url_for('cart'))


@app.route('/add-to-cart', methods=["POST"])
@login_required
def buy_product():
    prod_id = request.form.get('id')
    if prod_id is not None:
        if 'cart' not in session:
            session['cart'] = []
        session['cart'].append(prod_id)
        if None in session['cart']:
            session['cart'].remove(None)
        db.change_quantity(prod_id, 1)
        session.modified = True
        res = db.get_prod_info(prod_id)
        flash(f"{res[0]['name']} добавлен в корзину", 'success')
    return redirect(url_for('cart'))


@app.route('/cart')
@login_required
def cart():
    cart = session.get('cart', [])
    if cart:
        return render_template('cart.html', cart=get_cart(cart))
    else:
        flash('Корзина пуста', 'unsuccess')
        return redirect(url_for('index'))


@app.route('/login',methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        flash('Вы уже авторизованы', 'success')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.get_user_by_email(form.email.data)
        if user and check_password_hash(user['password'], form.password.data):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            flash('Успешный вход', 'success')
            return redirect(url_for('index'))
        flash('Неверный пароль', 'unsuccess')
    return render_template('login.html', form=form)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data)
        res = db.add_user(form.name.data, form.email.data, password)
        if res:
            flash('Вы успешно зарегистрированы', 'success')
            return redirect(url_for('login'))
        else:
            flash(f"Пользователь с email {form.email.data} уже существует", 'unsuccess')
    return render_template('registration.html', form=form)


def get_cart(cart):
    res = db.get_cart_sql(cart)
    return res


if __name__ == '__main__':
    db = DataBase(url)
    app.run(debug=True)