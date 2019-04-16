#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Authors:      Luis Carles Durá, Jaime García Velázquez, Manuel Martín Malagón, Rafael Rodríguez Sánchez
# Created:      2019/04/11
# Last update:  2019/04/16


import json

class DataLoader:

    def __init__(self):
        try:
            with open('data/products.json', encoding='utf-8') as data:
                self.products = json.load(data)
            with open('data/product_categories.json', encoding='utf-8') as data:
                self.product_categories = json.load(data)
            with open('data/orders.json', encoding='utf-8') as data:
                self.orders = json.load(data)
            with open('data/orders_record.json', encoding='utf-8') as data:
                self.orders_record = json.load(data)
            with open('data/tables.json', encoding='utf-8') as data:
                self.tables = json.load(data)
            with open('data/order_states.json', encoding='utf-8') as data:
                self.order_states = json.load(data)
        except:
            print("Error while reading web application data.")
            raise