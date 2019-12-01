from model.baseModel import Model


class Customer:
    def __init__(self, first_name: str, last_name: str, delivery_address: str, email: str, phone: str, id=''):
        self.first_name = first_name
        self.last_name = last_name
        self.delivery_address = delivery_address
        self.email = email
        self.phone = phone
        self.id = id

    @classmethod
    def from_dictionary(cls, dictionary):
        return cls(dictionary['first_name'], dictionary['last_name'], dictionary['delivery_address'],
                   dictionary['email'], dictionary['phone'], dictionary['id'])

    def __str__(self):
        res = str(self.id)
        res += '|First Name:' + self.first_name.replace('\n', '') if self.first_name is not None else ''
        res += ' |Last Name:' + self.last_name.replace('\n', '') if self.last_name is not None else ''
        res += ' |Delivery Address:' + self.delivery_address.replace('\n', '') \
            if self.delivery_address is not None else ''
        res += ' |Email:' + self.email.replace('\n', '') if self.email is not None else ''
        res += ' |Phone:' + self.phone.replace('\n', '') if self.phone is not None else ''
        return res


class CustomerModel(Model):
    def __init__(self, connection):
        super().__init__(connection)
        self.__insert_query = 'INSERT INTO customers (first_name, last_name, delivery_address, email, phone) ' \
                'VALUES( %(first_name)s, %(last_name)s, %(delivery_address)s, %(email)s, %(phone)s)'

    def get_all(self):
        query = 'SELECT * FROM customers ORDER BY id'
        self.cursor.execute(query)
        customers = []

        row = self.cursor.fetchone()
        while row is not None:
            customers.append(Customer.from_dictionary(row))
            row = self.cursor.fetchone()
        return customers

    def get_one(self, entity_id):
        query = 'SELECT * FROM customers ' \
                'WHERE id = %s'
        self.cursor.execute(query, [entity_id])
        row = self.cursor.fetchone()
        if row is None:
            raise Exception(f'Item id is incorrect: {entity_id}')
        return Customer.from_dictionary(row)

    def insert(self, entity):
        query = self.__insert_query
        self.cursor.execute(query, entity.__dict__)
        self.connection.commit()
        self.cursor.execute('SELECT LASTVAL()')
        return self.cursor.fetchone()['lastval']

    def update(self, entity):
        query = 'UPDATE customers ' \
                'SET first_name = %(first_name)s, last_name = %(last_name)s, delivery_address = %(delivery_address)s, ' \
                'email = %(email)s, phone = %(phone)s ' \
                'WHERE Id = %(id)s'
        self.cursor.execute(query, entity.__dict__)
        self.connection.commit()

    def delete(self, entity_id):
        query = 'DELETE FROM customers ' \
                'WHERE Id = %s'
        self.cursor.execute(query, [entity_id])
        self.connection.commit()

    def create_many(self, items):
        self.cursor.executemany(self.__insert_query, [item.__dict__ for item in items])
        self.connection.commit()
