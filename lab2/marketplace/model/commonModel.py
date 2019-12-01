from psycopg2.extras import DictCursor

from model.orders import Order
from model.products import Product


class CommonModel:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor(cursor_factory=DictCursor)

    def __del__(self):
        self.cursor.close()

    def fulltext_search_excluded(self, search: str):
        words = search.split()
        if len(words) > 0:
            words[0] = "!" + words[0]
        counter = 1
        while counter < len(words):
            words[counter] = "& !" + words[counter]
        search = ' '.join(words)
        query_excluding = "SELECT *, ts_headline(description, q) AS description " \
                          "FROM products, to_tsquery('english', %s) AS q " \
                          "WHERE to_tsvector('english', description) @@ q "
        self.cursor.execute(query_excluding, [search])
        products = []
        row = self.cursor.fetchone()
        while row is not None:
            products.append(Product.from_dictionary(row))
            row = self.cursor.fetchone()
        if len(products) > 0:
            return products
        else:
            raise Exception("There are no items")

    def fulltext_full_phrase(self, search):
        query_excluding = "SELECT *, ts_headline(description, q, 'StartSel=<<, StopSel=>>') AS description " \
                          "FROM products, phraseto_tsquery('english', %s) AS q " \
                          "WHERE to_tsvector('english', description) @@ q "
        self.cursor.execute(query_excluding, [search])
        products = []
        row = self.cursor.fetchone()
        while row is not None:
            products.append(Product.from_dictionary(row))
            row = self.cursor.fetchone()
        if len(products) > 0:
            return products
        else:
            raise Exception("There are no items")

    def search_by_multiple_attributes(self, date_from, date_to, approved):
        query = "SELECT * FROM orders WHERE (date BETWEEN %s AND %s) AND approved = %s"
        self.cursor.execute(query, [date_from, date_to, approved])
        orders = []
        row = self.cursor.fetchone()
        while row is not None:
            orders.append(Order.from_dictionary(row))
            row = self.cursor.fetchone()
        if len(orders) > 0:
            return orders
        else:
            raise Exception("There are no items")
