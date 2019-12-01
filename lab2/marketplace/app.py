import psycopg2

from controller.baseController import Controller

connection = None
try:
    connection = psycopg2.connect(host="localhost", port="5433",
                                  database="marketplace v3", user="postgres", password="12345678")
except (Exception, psycopg2.Error) as error:
    print("PostgresSQL Error: ", error)
finally:
    if connection is None:
        print("Couldn't connect to database, aborting...")
        exit(1)
    else:
        print("Opened connection with PostgresSQL")

controller = Controller(connection, 'Test')
controller.start()








#####################
# shopModel = ShopsModel(connection)

'''
shops = shopModel.get_all()
print(shops[0].name)
'''