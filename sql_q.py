GET_POPULAR_PRODUCTS = ('select * from products order by stock_quantity desc;')
GET_CHEAP_PRODUCTS = ('select * from products order by price;')
GET_EXPENSIVE_PRODUCTS = ('select * from products order by price desc;')
