#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Authors:      Luis Carles Durá, Jaime García Velázquez, Manuel Martín Malagón, Rafael Rodríguez Sánchez
# Created:      2019/04/10
# Last update:  2019/04/17


import os
import collections

from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory
from loaders.data_loader import DataLoader

try:
    data = DataLoader()
except:
    exit()

app = Flask(__name__)


'''
aux = list()

for product in data.products:
    aux.append(int(product))

print(max(aux))
'''


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"),
                               "favicon.ico", mimetype="image/vnd.microsoft.icon")


@app.route("/")
def root():
    return redirect("/index.html")


@app.route("/index.html")
def index():
    return render_template("/index.html", title="Inicio",
                           img_viewer=False, fixed_navbar=False,
                           customer=True)


@app.route("/about.html")
def about():
    return "!", 200


@app.route("/waiter")
def waiter_root():
    return redirect("/waiter/home.html")


@app.route("/waiter/home.html")
def waiter_home():
    return render_template("/waiter/home.html", title="Camarero",
                           img_viewer=False, fixed_navbar=False,
                           customer=False)


@app.route("/waiter/tables/list.html")
def waiter_tables():
    for table_id, table in data.tables.items():
        count = 0
        for order_id, order in data.orders.items():
            if(order["table_id"] == table_id):
                for order_record in data.orders_record.values():
                    if(order_record["order_id"] == order_id and
                       (order_record["state"] == "pending" or
                            order_record["state"] == "ear_kitchen")):
                        count = count + 1
        table["notifications"] = count
    return render_template("/tables/list.html", title="Mesas",
                           img_viewer=False, fixed_navbar=True,
                           tables=data.tables, customer=False)


@app.route("/waiter/tables/<num>/info.html", methods=['GET', 'POST'])
def waiter_table(num):
    if num in data.tables:
        if(request.method == 'POST' and "state" in request.form and "record-id" in request.form and
           request.form["state"] in data.order_states and request.form["record-id"] in data.orders_record):
            data.orders_record[request.form["record-id"]
                               ]["state"] = request.form["state"]
        return render_template("/tables/info.html", title="Mesa "+num,
                               num=num, img_viewer=True, fixed_navbar=True,
                               states=data.order_states,
                               orders=collections.OrderedDict(
                                   reversed(list(data.orders.items()))),
                               orders_record=collections.OrderedDict(
                                   reversed(list(data.orders_record.items()))),
                               products=data.products,
                               customer=False)
    else:
        abort(404)


@app.route("/waiter/orders/list.html")
def waiter_orders():
    for order in data.orders.values():
        order["total"] = 0.0
    for order_record in data.orders_record.values():
        if(order_record["state"] in data.order_states and order_record["state"] != "cancelled"):
            data.orders[order_record["order_id"]]["total"] = data.orders[order_record["order_id"]
                                                                         ]["total"] + order_record["product_price"]
    return render_template("/orders/list.html", title="Pedidos",
                           img_viewer=True, fixed_navbar=True,
                           categories=data.product_categories,
                           states=data.order_states,
                           orders=collections.OrderedDict(
                               reversed(list(data.orders.items()))),
                           orders_record=collections.OrderedDict(
                               reversed(list(data.orders_record.items()))),
                           products=data.products,
                           customer=False)


@app.route("/waiter/products/list.html", methods=['GET', 'POST'])
def waiter_products():
    if(request.method == 'POST' and "current-category" in request.form and
       "product-id" in request.form and request.form["product-id"] in data.products and
       request.form["current-category"] in data.product_categories):
        if("product-price" in request.form and isfloat(request.form["product-price"])):
            data.products[request.form["product-id"]
                          ]["price"] = float(request.form["product-price"])
        else:
            data.products[request.form["product-id"]
                          ]["available"] = not data.products[request.form["product-id"]
                                                             ]["available"]
        for category in data.product_categories:
            if(category == request.form["current-category"]):
                data.product_categories[category]["active"] = True
            else:
                data.product_categories[category]["active"] = False
    else:
        for category in data.product_categories:
            if(category == "drinks"):
                data.product_categories[category]["active"] = True
            else:
                data.product_categories[category]["active"] = False
    return render_template("/products/list.html", title="Productos",
                           img_viewer=True, fixed_navbar=True,
                           categories=data.product_categories,
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
                           img_viewer=False, fixed_navbar=False,
                           customer=True)


@app.route("/customer/products/list.html", methods=['GET', 'POST'])
def products_list():
    for category in data.product_categories:
        if(category == "drinks"):
            data.product_categories[category]["active"] = True
        else:
            data.product_categories[category]["active"] = False
    return render_template("/products/list.html", title="Productos",
                           img_viewer=True, fixed_navbar=True,
                           categories=data.product_categories,
                           products=data.products,
                           customer=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
