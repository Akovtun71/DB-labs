from model.orders import Order


class OrderController:
    def get_input_items(self, item: object = None):
        prompts = ['Product', 'Customer', 'Date', 'Approved']
        values = [item.product, item.customer, item.date, item.approved] \
            if isinstance(item, Order) else None
        return prompts, values

    def create_obj_from_input(self, input_items):
        product = customer = date = approved = None
        for item in input_items:
            if item['name'] == 'Product':
                product = int(item['value']) if item['value'] is not None else None
            elif item['name'] == 'Customer':
                customer = int(item['value']) if item['value'] is not None else None
            elif item['name'] == 'Date':
                date = str(item['value'])
            elif item['name'] == 'Approved':
                approved = bool(item['value']) if item['value'] is not None else False

        return Order(product, customer, date, approved)