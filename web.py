#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Authors:      Luis Carles Durá, Jaime García Velázquez, Manuel Martín Malagón, Rafael Rodríguez Sánchez
# Created:      2019/04/10
# Last update:  2019/04/16


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
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/")
def root():
    return redirect("/index.html")


@app.route("/index.html")
def index():
    return render_template("/index.html", title="Inicio",
                           img_viewer=False, fixed_navbar=False)


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


@app.route("/waiter/products/list.html", methods=['GET', 'POST'])
def waiter_dish():
    if(request.method == 'POST' and "current-category" in request.form and
       "product-id" in request.form and request.form["product-id"] in data.products and
       request.form["current-category"] in data.categories):
        if("product-price" in request.form):
            data.products[request.form["product-id"]
                          ]["price"] = float(request.form["product-price"])
        else:
            data.products[request.form["product-id"]
                          ]["available"] = not data.products[request.form["product-id"]
                                                             ]["available"]
        for category in data.categories:
            if(category == request.form["current-category"]):
                data.categories[category]["active"] = True
            else:
                data.categories[category]["active"] = False
    else:
        for category in data.categories:
            if(category == "drinks"):
                data.categories[category]["active"] = True
            else:
                data.categories[category]["active"] = False
    return render_template("/products/list.html", title="Productos",
                           img_viewer=True, fixed_navbar=True,
                           categories=data.categories,
                           products=data.products,
                           customer=False)


@app.route("/waiter/products/menu/list.html")
def waiter_menu():
    return "!", 200


@app.route("/customer")
def customer_root():
    return redirect("/customer/home.html")


@app.route("/customer/home.html")
def customer_home():
    return render_template("/customer/home.html", title="Cliente",
                           img_viewer=False, fixed_navbar=False)


@app.route("/customer/products/list.html", methods=['GET', 'POST'])
def products_list():
    for category in data.categories:
        if(category == "drinks"):
            data.categories[category]["active"] = True
        else:
            data.categories[category]["active"] = False
    return render_template("/products/list.html", title="Productos",
                           img_viewer=True, fixed_navbar=True,
                           categories=data.categories,
                           products=data.products,
                           customer=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
