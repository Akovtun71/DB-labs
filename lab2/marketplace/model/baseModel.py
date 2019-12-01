from abc import ABC

from psycopg2.extras import DictCursor


class Model(ABC):
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor(cursor_factory=DictCursor)

    def __del__(self):
        self.cursor.close()

    def get_all(self):
        pass

    def get_one(self, entity_id):
        pass

    def insert(self, entity):
        pass

    def update(self, entity):
        pass

    def delete(self, entity_id):
        pass

    def create_many(self, items):
        pass

