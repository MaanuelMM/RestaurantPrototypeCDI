#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Authors:      Luis Carles Durá, Jaime García Velázquez, Manuel Martín Malagón, Rafael Rodríguez Sánchez
# Created:      2019/04/11
# Last update:  2019/04/13


import json

class DataLoader:

    def __init__(self):
        try:
            with open('data/products.json', encoding='utf-8') as data:
                self.products = json.load(data)
            with open('data/categories.json', encoding='utf-8') as data:
                self.categories = json.load(data)
        except:
            print("Error while reading web application data.")
            raise