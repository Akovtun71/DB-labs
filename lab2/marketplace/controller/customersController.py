from model.customers import Customer
import json
import urllib.request


class CustomerController:
    def get_input_items(self, item: object = None):
        prompts = ['First Name', 'Last Name', 'Delivery Address', 'Email', 'Phone']
        values = [item.first_name, item.last_name, item.delivery_address, item.email, item.phone] \
            if isinstance(item, Customer) else None
        return prompts, values

    def create_obj_from_input(self, input_items):
        first_name = last_name = delivery_address = email = phone = None
        for item in input_items:
            if item['name'] == 'First Name':
                first_name = str(item['value'])
            elif item['name'] == 'Last Name':
                last_name = str(item['value'])
            elif item['name'] == 'Delivery Address':
                delivery_address = str(item['value'])
            elif item['name'] == 'Email':
                email = str(item['value'])
            elif item['name'] == 'Phone':
                phone = str(item['value'])
        return Customer(first_name, last_name, delivery_address, email, phone)

    @staticmethod
    def generate_random_items(count):
        url = f"https://randomuser.me/api/?nat=gb&results={count}&noinfo"
        content = CustomerController.get_content(url)
        items = []
        for item in content['results']:
            name = item['name']
            first_name = name['first']
            last_name = name['last']
            location = item['location']
            delivery_address = location['country'] + ', ' \
                               + location['city'] + ', ' \
                               + location['street']['name'] + ', ' \
                               + str(location['street']['number'])
            email = item['email']
            phone = item['phone']
            items.append(Customer(first_name, last_name, delivery_address, email, phone))
        return items

    @staticmethod
    def get_content(url: str):
        req = urllib.request.Request(url)
        r = urllib.request.urlopen(req).read()
        return json.loads(r.decode('utf-8'))
