from model.baseModel import Model


class Product:
    def __init__(self, name: str, price: float, description: str, quantity: int, shop: int, photo_url: str, id=''):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity
        self.shop = shop
        self.photo_url = photo_url
        self.id = id

    @classmethod
    def from_dictionary(cls, dictionary):
        return cls(dictionary['name'], dictionary['price'], dictionary['description'], dictionary['quantity'],
                   dictionary['shop'], dictionary['photo_url'], dictionary['id'])

    def __str__(self):
        res = str(self.id)
        res += '|Name:' + self.name.replace('\n', '') if self.name is not None else ''
        res += ' |Price:' + str(self.price) if self.price is not None else ''
        res += ' |Description:' + self.description.replace('\n', '') if self.description is not None else ''
        res += ' |Quantity:' + str(self.quantity) if self.quantity is not None else ''
        res += ' |Shop:' + str(self.shop) if self.shop is not None else ''
        res += ' |Photo:' + self.photo_url.replace('\n', '') if self.photo_url is not None else ''
        return res


class ProductModel(Model):
    def get_all(self):
        query = 'SELECT * FROM products ORDER BY id'
        self.cursor.execute(query)
        products = []

        row = self.cursor.fetchone()
        while row is not None:
            products.append(Product.from_dictionary(row))
            row = self.cursor.fetchone()
        return products

    def get_one(self, entity_id):
        query = 'SELECT * FROM products ' \
                'WHERE id = %s'
        self.cursor.execute(query, [entity_id])
        row = self.cursor.fetchone()
        if row is None:
            raise Exception(f'Item id is incorrect: {entity_id}')
        return Product.from_dictionary(row)

    def insert(self, entity):
        query = 'INSERT INTO products (name, price, description, quantity, shop, photo_url) ' \
                'VALUES( %(name)s, %(price)s, %(description)s, %(quantity)s, %(shop)s, %(photo_url)s)'
        self.cursor.execute(query, entity.__dict__)
        self.connection.commit()
        self.cursor.execute('SELECT LASTVAL()')
        return self.cursor.fetchone()['lastval']

    def update(self, entity):
        query = 'UPDATE products ' \
                'SET name = %(name)s, price = %(price)s, description = %(description)s, ' \
                'quantity = %(quantity)s, shop = %(shop)s, photo_url = %(photo_url)s ' \
                'WHERE Id = %(id)s'
        self.cursor.execute(query, entity.__dict__)
        self.connection.commit()

    def delete(self, entity_id):
        query = 'DELETE FROM products ' \
                'WHERE Id = %s'
        self.cursor.execute(query, [entity_id])
        self.connection.commit()
