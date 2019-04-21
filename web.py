#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Authors:      Luis Carles Durá, Jaime García Velázquez, Manuel Martín Malagón, Rafael Rodríguez Sánchez
# Created:      2019/04/10
# Last update:  2019/04/20


import os
import datetime
import collections

from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory
from loaders.data_loader import DataLoader

try:
    data = DataLoader()
except:
    exit()

app = Flask(__name__)


def change_table_status(table_id):
    data.tables[table_id]["occupied"] = not data.tables[table_id]["occupied"]
    data.tables[table_id]["relative_height"] = 50
    data.tables[table_id]["first_heath_section"] = False
    data.tables[table_id]["second_heath_section"] = False
    data.tables[table_id]["third_heath_section"] = False
    data.tables[table_id]["fourth_heath_section"] = False


def new_order(table_id):
    aux = list()
    for order_id in data.orders:
        aux.append(int(order_id))
    aux = str(max(aux) + 1)
    data.orders[aux] = dict()
    data.orders[aux]["date_time"] = str(datetime.datetime.now())
    data.orders[aux]["bill_requested"] = False
    data.orders[aux]["pay_by_card"] = False
    data.orders[aux]["paid"] = False
    data.orders[aux]["invoice"] = False
    data.orders[aux]["table_id"] = table_id
    return aux

def new_order_record(table_id, product_id, product_price):
    #busca la order_id activa para la mesa
    aux = list()
    for orders_record_id in data.orders_record:
        aux.append(int(orders_record_id))
    aux = str(max(aux) + 1)
    data.orders[aux] = dict()
    data.orders[aux]["order_id"] = order_id
    data.orders[aux]["product_id"] = product_id
    data.orders[aux]["product_price"] = product_price
    data.orders[aux]["state"] = "pending"
    return aux

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def count_notifications_table():
    for table_id, table in data.tables.items():
        count = 0
        for order_id, order in data.orders.items():
            if order["table_id"] == table_id:
                if order["bill_requested"] and not order["paid"]:
                    count = count + 1
                for order_record in data.orders_record.values():
                    if(order_record["order_id"] == order_id and
                       (order_record["state"] == "pending" or
                            order_record["state"] == "ear_kitchen")):
                        count = count + 1
        table["notifications"] = count


def make_active_product_category(active_category):
    for category in data.product_categories:
        if(category == active_category):
            data.product_categories[category]["active"] = True
        else:
            data.product_categories[category]["active"] = False


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
    count_notifications_table()
    return render_template("/tables/list.html", title="Mesas",
                           img_viewer=False, fixed_navbar=True,
                           tables=data.tables, customer=False)


@app.route("/waiter/tables/<num>/info.html", methods=['GET', 'POST'])
def waiter_table(num):
    if num in data.tables:
        if request.method == 'POST':
            if("state" in request.form and "record-id" in request.form and
               request.form["state"] in data.order_states and
               request.form["record-id"] in data.orders_record):
                data.orders_record[request.form["record-id"]
                                   ]["state"] = request.form["state"]
            elif("order-id" in request.form and "paid" in request.form and
                 request.form["order-id"] in data.orders and request.form["paid"].lower() == "true"):
                data.orders[request.form["order-id"]]["paid"] = True
                change_table_status(
                    data.orders[request.form["order-id"]]["table_id"])
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
        make_active_product_category(request.form["current-category"])
    else:
        make_active_product_category("drinks")
    return render_template("/products/list.html", title="Productos",
                           img_viewer=True, fixed_navbar=True,
                           categories=data.product_categories,
                           products=data.products,
                           customer=False)


@app.route("/customer")
def customer_root():
    return redirect("/customer/home.html")


@app.route("/customer/home.html", methods=['GET', 'POST'])
def customer_home():
    if(request.method == 'POST' and "table-id" in request.form and request.form["table-id"] in data.tables):
        return redirect("/customer/tables/" + request.form["table-id"] + "/home.html")
    else:
        return render_template("/customer/home.html", title="Cliente",
                               img_viewer=False, fixed_navbar=False,
                               customer=True, tables=data.tables)


@app.route("/customer/tables/<num>/home.html")
def customer_table(num):
    if num in data.tables:
        return render_template("/tables/home.html", title="Mesa "+num,
                               img_viewer=False, fixed_navbar=False,
                               customer=True, tables=data.tables,
                               num=num)
    else:
        abort(404)


@app.route("/customer/tables/<num>/edit.html", methods=['GET', 'POST'])
def customer_table_edit(num):
    if num in data.tables:
        if request.method == 'POST':
            if "height" in request.form:
                if request.form["height"] == "up" and data.tables[num]["relative_height"] != 100:
                    data.tables[num]["relative_height"] = data.tables[num]["relative_height"] + 10
                elif request.form["height"] == "down" and data.tables[num]["relative_height"] != 0:
                    data.tables[num]["relative_height"] = data.tables[num]["relative_height"] - 10
            elif "first_heath_section" in request.form:
                data.tables[num]["first_heath_section"] = not data.tables[num]["first_heath_section"]
            elif "second_heath_section" in request.form:
                data.tables[num]["second_heath_section"] = not data.tables[num]["second_heath_section"]
            elif "third_heath_section" in request.form:
                data.tables[num]["third_heath_section"] = not data.tables[num]["third_heath_section"]
            elif "fourth_heath_section" in request.form:
                data.tables[num]["fourth_heath_section"] = not data.tables[num]["fourth_heath_section"]
        return render_template("/tables/edit.html", title="Mesa "+num,
                               img_viewer=False, fixed_navbar=True,
                               customer=True, tables=data.tables,
                               num=num)
    else:
        abort(404)


@app.route("/customer/tables/<num>/info.html")
def customer_table_info(num):
    #busca la order_id activa para la mesa
    paid=data.orders[order_id]["bill_requested"]
    if num in data.tables:
        return render_template("/tables/info.html", title="Mesa "+num,
                               num=num, img_viewer=True, fixed_navbar=True,
                               states=data.order_states,
                               orders=collections.OrderedDict(
                                   reversed(list(data.orders.items()))),
                               orders_record=collections.OrderedDict(
                                   reversed(list(data.orders_record.items()))),
                               products=data.products,
                               customer=True, paid=paid)
    else:
        abort(404)


@app.route("/customer/<num>/products/list.html", methods=['GET', 'POST'])
def products_list(num):
    if num in data.tables:
        for category in data.product_categories:
            if(category == "drinks"):
                data.product_categories[category]["active"] = True
            else:
                data.product_categories[category]["active"] = False
        return render_template("/products/list.html", title="Productos",
                               img_viewer=True, fixed_navbar=True,
                               categories=data.product_categories,
                               products=data.products,
                               customer=True, num=num)
    else:
        abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
