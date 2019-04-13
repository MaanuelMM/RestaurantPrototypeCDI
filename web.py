#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Authors:      Luis Carles Durá, Jaime García Velázquez, Manuel Martín Malagón, Rafael Rodríguez Sánchez
# Created:      2019/04/10
# Last update:  2019/04/13


import os

from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory
from loaders.data_loader import DataLoader

try:
    data = DataLoader()
except:
    exit()

app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route("/")
def root():
    return redirect("/index.html")

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/about.html")
def about():
    return "!", 200

@app.route("/waiter")
def waiter_root():
    return redirect("/waiter/home.html")

@app.route("/waiter/home.html")
def waiter_home():
    return "!", 200

@app.route("/waiter/products/home.html")
def waiter_products():
    return "!", 200

@app.route("/waiter/products/dish/list.html")
def waiter_dish():
    return "!", 200

@app.route("/waiter/products/menu/list.html")
def waiter_menu():
    return "!", 200

@app.route("/customer")
def customer_root():
    return redirect("/customer/home.html")

@app.route("/customer/home.html")
def customer_home():
    return "!", 200

@app.route("/products/list.html")
def products_list():
    return render_template("/products/list.html", categories=data.categories,
                           products=data.products)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)