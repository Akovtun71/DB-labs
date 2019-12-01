from model.shops import Shop


class ShopController:
    def get_input_items(self, item: object = None):
        prompts = ['Name', 'Website URL', 'Image URL']
        values = [item.name, item.website_url, item.image_url] if isinstance(item, Shop) else None
        return prompts, values

    def create_obj_from_input(self, input_items):
        name = website_url = img_url = None
        for item in input_items:
            if item['name'] == 'Name':
                name = str(item['value'])
            elif item['name'] == 'Website URL':
                website_url = str(item['value'])
            elif item['name'] == 'Image URL':
                img_url = str(item['value'])

        return Shop(name, website_url, img_url)
