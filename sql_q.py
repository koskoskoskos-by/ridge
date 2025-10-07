import psycopg
from psycopg.rows import dict_row
import datetime


class DataBase:
    def __init__(self, url):
        self.url = url

    def query_commit(self, query):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
            conn.commit()
            return True

    def connect(self):
        return psycopg.connect(self.url, row_factory=dict_row)

    def select_all(self, query, params=None):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()

    def select_one(self,query,params=None):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchone()

    def sort_by(self, sort_by):
        query = f"select * from products order by {sort_by}"
        return self.select_all(query)

    def change_quantity(self, id, value):
        query = f"update products set stock_quantity = stock_quantity - {value} WHERE id = {id}"
        return self.query_commit(query)

    def get_user(self, id):
        query = f"select * from users where id = '{id}'"
        return self.select_one(query)

    def add_user(self, name, email, password):
        query = f"select count(*) from users where email = '{email}'"
        res = self.select_one(query)
        print(res)
        if res[0]['count'] > 0:
            return False
        date = datetime.date.today()
        query = f"insert into users(name, email, password, created_at) values('{name}', '{email}', '{password}', '{date}')"
        return self.query_commit(query)

    def get_prod_info(self, prod_id):
        query = f"select * from products where id = {prod_id}"
        return self.select_one(query)

    def get_user_by_email(self, email):
        query = f"select * from users where email = '{email}'"
        return self.select_one(query)

    def get_cart(self,user_id):
        query = f"select cart_id from shopping_cart where user_id = {user_id}"
        return self.select_one(query)

    def add_cart(self, user_id):
        date = datetime.date.today()
        query = f"insert into shopping_cart(user_id, created_at) values('{user_id}', '{date}')"
        return self.query_commit(query)

    def add_product(self, cart_id, prod_id):
        query = f"insert into cart_items(cart_id, product_id) values({cart_id}, {prod_id})"
        return self.query_commit(query)

    def get_products_in_cart(self, user_id):
        query = f"select * from products join cart_items on products.id = cart_items.product_id " \
                f"join shopping_cart on shopping_cart.cart_id = cart_items.cart_id " \
                f"where shopping_cart.user_id = {user_id}"
        return self.select_all(query)

    def del_product_from_cart(self, cart_id, prod_id):
        query = f"delete from cart_items where cart_item_id = (select cart_item_id from cart_items " \
                f"where cart_id = {cart_id} and product_id = {prod_id} limit 1) "
        return self.query_commit(query)

    def search_products(self, search):
        query = f"select* from products where name ilike '{search}%'"
        return self.select_all(query)

    def get_prod_by_slug(self, slug):
        query = f"select * from products where slug = '{slug}'"
        return self.select_one(query)

    def count_products(self,user_id):
        query = f"select name, price, id, count(id) as number, stock_quantity, image_url from products " \
                f"join cart_items on products.id = cart_items.product_id " \
                f"join shopping_cart on shopping_cart.cart_id = cart_items.cart_id " \
                f"where shopping_cart.user_id = {user_id} group by id"
        return self.select_all(query)

    def get_users(self):
        query = f"select * from users"
        return self.select_all(query)

    def get_products(self):
        query = f"select * from products"
        return self.select_all(query)

    def create_product(self, name, description, price, stock_quantity, image_url, slug):
        query = f"insert into products(name, description, price, stock_quantity, image_url, slug)" \
                f"values('{name}', '{description}', {price}, {stock_quantity}, '{image_url}', '{slug}')"
        return self.query_commit(query)