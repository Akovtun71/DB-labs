from model.products import Product


class ProductController:
    def get_input_items(self, item: object = None):
        prompts = ['Name*', 'Price', 'Description', 'Quantity', 'Shop*', 'Photo URL']
        values = [item.name, item.price, item.description, item.quantity, item.shop, item.photo_url] \
            if isinstance(item, Product) else None
        return prompts, values

    def create_obj_from_input(self, input_items):
        name = price = description = quantity = shop = photo_url = None
        for item in input_items:
            if item['name'] == 'Name*':
                name = str(item['value'])
            elif item['name'] == 'Price':
                price = float(item['value']) if item['value'] is not None else 0
            elif item['name'] == 'Description':
                description = str(item['value'])
            elif item['name'] == 'Quantity':
                quantity = int(item['value']) if item['value'] is not None else 0
            elif item['name'] == 'Shop*':
                shop = int(item['value']) if item['value'] is not None else None
            elif item['name'] == 'Photo URL':
                photo_url = str(item['value'])

        return Product(name, price, description, quantity, shop, photo_url)
