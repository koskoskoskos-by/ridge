from flask import Flask, render_template, url_for, request, flash, session, redirect
from sql_q import *
from forms import *
from werkzeug.security import check_password_hash,generate_password_hash
from User import *
from flask_login import LoginManager, login_manager, login_user, login_required, current_user, logout_user

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
    id = current_user.get_id()
    cart = db.get_cart(id)
    db.del_product_from_cart(cart['cart_id'], int(prod_id))
    db.change_quantity(prod_id, -1)
    if db.get_products_in_cart(cart['cart_id']) is None:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('cart'))


@app.route('/add-to-cart', methods=["POST"])
@login_required
def buy_product():
    prod_id = request.form.get('id')
    id = current_user.get_id()
    if db.get_cart(id) is None:
        db.add_cart(id)
    cart = db.get_cart(id)
    db.add_product(cart['cart_id'], int(prod_id))
    db.change_quantity(prod_id, 1)
    res = db.get_prod_info(prod_id)
    flash(f"{res['name']} добавлен в корзину", 'success')
    return redirect(url_for('cart'))


@app.route('/cart')
@login_required
def cart():
    user_id = current_user.get_id()
    cart = db.get_products_in_cart(int(user_id))
    if cart:
        return render_template('cart.html', cart=cart)
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


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/profile")
@login_required
def profile():
    user = db.get_user(current_user.get_id())
    return render_template('profile.html', user=user)


@app.route("/search")
def search():
    search = request.args.get('query', '').strip()
    if not search:
        return redirect(url_for('index'))
    res = db.search_products(search)
    print(res)
    return render_template('search.html', search=res)


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Пожалуйста, войдите в аккаунт, чтобы получить доступ к этой странице.', 'unsuccess')
    return redirect(url_for('login'))


if __name__ == '__main__':
    db = DataBase(url)
    app.run(debug=True)