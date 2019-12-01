from model.baseModel import Model


class Shop:
    def __init__(self, name: str, website_url: str, image_url: str, id: int = ''):
        self.name = name
        self.website_url = website_url
        self.image_url = image_url
        self.id = id

    @classmethod
    def from_dictionary(cls, dictionary):
        return cls(dictionary['shop_name'], dictionary['website_url'], dictionary['image_url'], dictionary['id'])

    def __str__(self):
        res = str(self.id)
        res += '|Name:' + self.name.replace('\n', '') if self.name is not None else ''
        res += ' |Website:' + self.website_url.replace('\n', '') if self.website_url is not None else ''
        res += ' |Image:' + self.image_url.replace('\n', '') if self.image_url is not None else ''
        return res


class ShopModel(Model):
    def get_all(self):
        query = 'SELECT * FROM shops ORDER BY id'
        self.cursor.execute(query)
        shops = []

        row = self.cursor.fetchone()
        while row is not None:
            shops.append(Shop.from_dictionary(row))
            row = self.cursor.fetchone()
        return shops

    def get_one(self, entity_id: int):
        query = 'SELECT * FROM shops ' \
                'WHERE id = %s'
        self.cursor.execute(query, [entity_id])
        row = self.cursor.fetchone()
        if row is None:
            raise Exception(f'Item id is incorrect: {entity_id}')
        return Shop.from_dictionary(row)

    def insert(self, entity: object):
        query = 'INSERT INTO shops (shop_name, website_url, image_url) ' \
                'VALUES( %(name)s, %(website_url)s, %(image_url)s)'
        self.cursor.execute(query, entity.__dict__)
        self.connection.commit()
        self.cursor.execute('SELECT LASTVAL()')
        return self.cursor.fetchone()['lastval']

    def update(self, entity: object):
        query = 'UPDATE shops ' \
                'SET shop_name = %(name)s, website_url = %(website_url)s, image_url = %(image_url)s ' \
                'WHERE Id = %(id)s'
        self.cursor.execute(query, entity.__dict__)
        self.connection.commit()

    def delete(self, entity_id: int):
        query = 'DELETE FROM shops ' \
                'WHERE Id = %s'
        self.cursor.execute(query, [entity_id])
        self.connection.commit()
