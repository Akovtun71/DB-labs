from datetime import datetime

import psycopg2

from controller.shopsController import ShopController
from controller.customersController import CustomerController
from controller.ordersController import OrderController
from controller.productsController import ProductController
from model.baseModel import Model
from model.commonModel import CommonModel
from model.products import ProductModel
from typing import Tuple, Optional
from model.customers import CustomerModel
from model.orders import OrderModel
from model.shops import ShopModel
from view.baseView import View, ConsoleCommands, MessageType


class Controller:
    def __init__(self, connection, program_name):
        self.view = View(program_name)
        self.common_model = CommonModel(connection)
        self.connection = connection
        self.entities = ['Shops', 'Products', 'Customers', 'Orders']
        self.view.start_app()

    def start(self):
        list_menu = ['CRUD operations with relations', 'Batch generation of "randomized" data',
                     'Search by multiple attributes of two entities', 'Full text search']
        menu_option = self.view.draw_menu(list_menu, 'Main menu', True)
        if menu_option == 0:
            self.choose_entity_for_crud()
        elif menu_option == 1:
            self.__random_data_generation()
        elif menu_option == 2:
            self.__search_by_multiple_attributes()
        elif menu_option == 3:
            self.__fulltext_search()

    def choose_entity_for_crud(self):
        menu_option = self.view.draw_menu(self.entities, 'Choose entity')
        entity_model = None
        entity_controller = None
        if menu_option == 0:
            entity_model = ShopModel(self.connection)
            entity_controller = ShopController()
        elif menu_option == 1:
            entity_model = ProductModel(self.connection)
            entity_controller = ProductController()
        elif menu_option == 2:
            entity_model = CustomerModel(self.connection)
            entity_controller = CustomerController()
        elif menu_option == 3:
            entity_model = OrderModel(self.connection)
            entity_controller = OrderController()
        elif menu_option == ConsoleCommands.GO_BACK:
            return self.start()
        self.__choose_crud_operation(entity_model, entity_controller)

    def __choose_crud_operation(self, entity_model, entity_controller):
        crud_menu = ['Get all', 'Insert new', 'Update', 'Delete']
        run_crud_menu = True
        while run_crud_menu:
            menu_option = self.view.draw_menu(crud_menu, 'Choose operation')
            if menu_option == 0:
                self.__get_all_entities(entity_model)
            elif menu_option == 1:
                self.__insert_entity(entity_model, entity_controller)
            elif menu_option == 2:
                self.__update_entity(entity_model, entity_controller)
            elif menu_option == 3:
                self.__delete_entity(entity_model)
            elif menu_option == ConsoleCommands.GO_BACK:
                run_crud_menu = False
        return self.choose_entity_for_crud()

    def __get_all_entities(self, entity_model):
        all_entities = entity_model.get_all()
        output = ''
        for item in all_entities:
            output += str(item) + '\n'
        self.view.draw_text(output)

    def __insert_entity(self, entity_model, entity_controller):
        input_items = self.__get_input_items_form(entity_controller.get_input_items())
        command = self.view.draw_input(input_items, 'Create')
        if command == ConsoleCommands.CONFIRM:
            try:
                item = entity_model.insert(entity_controller.create_obj_from_input(input_items))
                message = f'Item was successfully created, id: '
                message += str(item)
                self.view.draw_text(message, MessageType.SUCCESSFUL)
            except (Exception, psycopg2.Error) as e:
                self.view.draw_text(str(e), MessageType.ERROR)

    def __update_entity(self, entity_model, entity_controller):
        question = f'Enter Id:'
        id = self.view.draw_modal_prompt(question, f'item')
        try:
            if isinstance(id, str):
                id = int(id)
            item = entity_model.get_one(id)
            input_items = self.__get_input_items_form(entity_controller.get_input_items(item))
            command = self.view.draw_input(input_items, 'Update')
            if command == ConsoleCommands.CONFIRM:
                entity = entity_controller.create_obj_from_input(input_items)
                entity.id = id
                entity_model.update(entity)
                message = f'Item was successfully updated: ({entity})'
                self.view.draw_text(message, MessageType.SUCCESSFUL)
        except (Exception, psycopg2.Error) as e:
            self.view.draw_text(str(e), MessageType.ERROR)

    def __delete_entity(self, entity_model):
        question = f'Enter Id:'
        id = self.view.draw_modal_prompt(question, f'item')
        try:
            if isinstance(id, str):
                id = int(id)
            item = entity_model.get_one(id)
            question = f'Enter Y to delete ({item})'
            confirm = self.view.draw_modal_prompt(question, f'Deleting item')
            if confirm.strip().lower() == "y":
                entity_model.delete(id)
                self.view.draw_text('Item was successfully deleted', MessageType.SUCCESSFUL)
        except (Exception, psycopg2.Error) as e:
            self.view.draw_text(str(e), MessageType.ERROR)

    def __random_data_generation(self):
        try:
            action_name = 'Batch generation of "randomized" data'
            num_str = self.view.draw_modal_prompt('Enter n > 0 - amount of items to generate:', action_name)
            n = int(num_str)
            if n <= 0:
                raise Exception(f'n should be > 0, got {n}')
            CustomerModel(self.connection).create_many(CustomerController.generate_random_items(n))
            self.view.draw_text('Items were successfully created', MessageType.SUCCESSFUL)

        except(Exception, psycopg2.Error) as e:
            self.view.draw_text(str(e), MessageType.ERROR)

    def __fulltext_search(self):
        list_menu = ['The word is not included', 'Full phrase']
        menu_option = self.view.draw_menu(list_menu, 'Full text search')
        if menu_option == 0:
            self.__fulltext_search_excluded()
        elif menu_option == 1:
            self.__fulltext_full_phrase()
        elif menu_option == ConsoleCommands.GO_BACK:
            self.start()

    def __fulltext_search_excluded(self):
        try:
            command = self.view.draw_modal_prompt('Enter query:', 'Fulltext search excluding words')
            res = self.common_model.fulltext_search_excluded(command)
            output = ''
            for item in res:
                output += str(item) + '\n'
            self.view.draw_text(output)
        except (Exception, psycopg2.Error) as e:
            self.view.draw_text(str(e), MessageType.ERROR)
        finally:
            self.__fulltext_search()

    def __fulltext_full_phrase(self):
        try:
            command = self.view.draw_modal_prompt('Enter query:', 'Full phrase search')
            res = self.common_model.fulltext_full_phrase(command)
            output = ''
            for item in res:
                output += str(item) + '\n'
            self.view.draw_text(output)
        except (Exception, psycopg2.Error) as e:
            self.view.draw_text(str(e), MessageType.ERROR)
        finally:
            self.__fulltext_search()

    def __search_by_multiple_attributes(self):
        prompts = ['Date from', 'Date to', 'Is approved']
        values = ['', '', 'n']
        input_items = self.__get_input_items_form((prompts, values))
        try:
            command = self.view.draw_input(input_items, 'Search attributes')
            if command == ConsoleCommands.CONFIRM:
                date_from = date_to = approved = None
                for item in input_items:
                    if item['name'] == 'Date from':
                        date_from = datetime.strptime(item['value'], '%d-%m-%Y').date() \
                            if item['value'] is not None else ''
                    elif item['name'] == 'Date to':
                        date_to = datetime.strptime(item['value'], '%d-%m-%Y').date() \
                            if item['value'] is not None else ''
                    elif item['name'] == 'Is approved':
                        approved_str = str(item['value']) if item['value'] is not None else ''
                        approved = approved_str.lower() == 'y' or approved_str.lower() == 'yes'

                res = self.common_model.search_by_multiple_attributes(date_from, date_to, approved)
                output = ''
                for item in res:
                    output += str(item) + '\n'
                self.view.draw_text(output)
        except (Exception, psycopg2.Error) as e:
            self.view.draw_text(str(e), MessageType.ERROR)
        finally:
            self.start()

    @staticmethod
    def __get_input_items_form(tup: Tuple[list, Optional[list]]):
        if tup[1] is None:
            return [{'name': name, 'value': None} for name in tup[0]]
        return [{'name': name, 'value': val} for name, val in zip(tup[0], tup[1])]

