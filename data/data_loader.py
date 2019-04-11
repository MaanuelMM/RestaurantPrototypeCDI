#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Authors:      Luis Carles Durá, Jaime García Velázquez, Manuel Martín Malagón, Rafael Rodríguez Sánchez
# Created:      2019/04/11
# Last update:  2019/04/11


import json

class DataLoader:

    def __init__(self):
        try:
            data = json.load(open('data/config.json'), encoding="utf-8")
            self.host = data["host"]
            self.user = data["user"]
            self.password = data["password"]
            self.port = data["port"]
            self.database = data["database"]
        except:
            print("Error al leer el archivo de configuración.")
            raise Exception()