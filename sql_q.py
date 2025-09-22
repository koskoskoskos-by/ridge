import datetime

import psycopg
from psycopg.rows import dict_row
from datetime import date

class DataBase:
    def __init__(self, url):
        self.url = url

    def connect(self):
        return psycopg.connect(self.url, row_factory=dict_row)

    def select(self, query, params=None):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                res = cur.fetchall()
                return res

    def sort_by(self, sort_by):
        query = f"select * from products order by {sort_by}"
        return self.select(query)

    def change_quantity(self, id, value):
        query = f"update products set stock_quantity = stock_quantity - {value} WHERE id = {id}"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
            conn.commit()
            return

    def get_user(self, id):
        query = f"select * from users where id = '{id}'"
        return self.select(query)

    def get_cart_sql(self, cart):
        if not cart:
            return
        placeholders = ','.join(['%s'] * len(cart))
        query = f"SELECT * FROM products WHERE id IN ({placeholders})"
        return self.select(query, tuple(cart))

    def add_user(self, name, email, password):
        query = f"select count(*) from users where email = '{email}'"
        res = self.select(query)
        print(res)
        if res[0]['count'] > 0:
            return False
        date = datetime.date.today()
        query = f"insert into users(name, email, password, created_at) values('{name}', '{email}', '{password}', '{date}')"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
            conn.commit()
            return True

    def get_prod_info(self,prod_id):
        query = f"select * from products where id = {prod_id}"
        return self.select(query)

    def get_user_by_email(self, email):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(f"select * from users where email = '{email}'")
                res = cur.fetchone()
                return res

