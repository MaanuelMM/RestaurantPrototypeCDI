#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Authors:      Luis Carles Durá, Jaime García Velázquez, Manuel Martín Malagón, Rafael Rodríguez Sánchez
# Created:      2019/04/11
# Last update:  2019/04/11


import mysql.connector

class MySQLConnector:

    def __init__(self, host, user, password, port, database):
        try:
            self.mydb = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                port=port,
                database=database
            )
            self.mycursor = self.mydb.cursor()
        except:
            print("Error al realizar la conexión con la base de datos.")
            raise