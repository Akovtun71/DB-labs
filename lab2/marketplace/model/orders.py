from model.baseModel import Model
import datetime


class Order:
    def __init__(self, product: int, customer: int, date: datetime, approved: bool = False, id: int = ''):
        self.product = product
        self.customer = customer
        self.date = date
        self.approved = approved
        self.id = id

    @classmethod
    def from_dictionary(cls, dictionary):
        return cls(dictionary['product'], dictionary['customer'],
                   dictionary['date'], dictionary['approved'], dictionary['id'])

    def __str__(self):
        res = str(self.id)
        res += '|Product:' + str(self.product) if self.product is not None else ''
        res += ' |Customer:' + str(self.customer) if self.customer is not None else ''
        res += ' |Date:' + str(self.date) if self.date is not None else ''
        res += ' |Approved:' + str(self.approved) if self.approved is not None else ''
        return res


class OrderModel(Model):
    def get_all(self):
        query = 'SELECT * FROM orders ORDER BY id'
        self.cursor.execute(query)
        orders = []

        row = self.cursor.fetchone()
        while row is not None:
            orders.append(Order.from_dictionary(row))
            row = self.cursor.fetchone()
        return orders

    def get_one(self, entity_id: int):
        query = 'SELECT * FROM orders ' \
                'WHERE id = %s'
        self.cursor.execute(query, [entity_id])
        row = self.cursor.fetchone()
        if row is None:
            raise Exception(f'Item id is incorrect: {entity_id}')
        return Order.from_dictionary(row)

    def insert(self, entity: object):
        query = 'INSERT INTO orders (product, customer, date, approved) ' \
                'VALUES( %(product)s, %(customer)s, %(date)s, %(approved)s)'
        self.cursor.execute(query, entity.__dict__)
        self.connection.commit()
        self.cursor.execute('SELECT LASTVAL()')
        return self.cursor.fetchone()['lastval']

    def update(self, entity: object):
        query = 'UPDATE orders ' \
                'SET product = %(product)s, customer = %(customer)s, date = %(date)s, approved = %(approved)s ' \
                'WHERE Id = %(id)s'
        self.cursor.execute(query, entity.__dict__)
        self.connection.commit()

    def delete(self, entity_id: int):
        query = 'DELETE FROM orders ' \
                'WHERE Id = %s'
        self.cursor.execute(query, [entity_id])
        self.connection.commit()
