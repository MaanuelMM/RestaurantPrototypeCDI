#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Authors:      Luis Carles Durá, Jaime García Velázquez, Manuel Martín Malagón, Rafael Rodríguez Sánchez
# Created:      2019/04/10
# Last update:  2019/04/22


import os
import datetime
import collections

from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory
from loaders.data_loader import DataLoader
from flask_sslify import SSLify


try:
    data = DataLoader()
except:
    exit()

app = Flask(__name__)

if 'DYNO' in os.environ:  # only trigger SSLify if the app is running on Heroku
    sslify = SSLify(app)


def order_has_pending_record(order_id):
    has_pending_record = False

    for order_record in data.orders_record.values():
        if order_record["order_id"] == order_id and (
                order_record["state"] == "pending" or order_record["state"] == "ear_kitchen"):
            has_pending_record = True
            break

    return has_pending_record


def order_has_cart_record(order_id):
    has_cart_record = False

    for order_record in data.orders_record.values():
        if order_record["order_id"] == order_id and order_record["state"] == "cart":
            has_cart_record = True
            break

    return has_cart_record


def order_has_record(order_id):
    has_record = False

    for order_record in data.orders_record.values():
        if order_record["order_id"] == order_id:
            has_record = True
            break

    return has_record


def table_is_occupied(table_id):
    latest_order_id = order_get_latest(table_id)
    data.tables[table_id]["occupied"] = order_is_valid(latest_order_id)


def tables_are_occupied():
    for table_id in data.tables:
        table_is_occupied(table_id)


def order_is_valid(order_id):
    # an order is valid if exists any order_record which state is "pending",
    # "ear_kitchen" or "delivered", and it's not being paid before

    is_valid = False

    if order_id and not data.orders[order_id]["paid"]:
        for order_record in data.orders_record.values():
            if(order_record["order_id"] == order_id and
                    order_record["state"] != "cancelled" and
                    order_record["state"] in data.order_states):
                is_valid = True
                break

    return is_valid


def order_get_latest(table_id):
    # data.orders is a dict that is ordered from old to new, so all
    # we have to do is to reverse it to get the latest known order

    latest_order_id = False

    for order_id, order in collections.OrderedDict(reversed(list(data.orders.items()))).items():
        if order["table_id"] == table_id:
            latest_order_id = order_id
            break

    return latest_order_id


def order_total_price(order_id, with_cart=False):
    total = 0.0

    for order_record in data.orders_record.values():
        if order_record["order_id"] == order_id:
            if order_record["state"] != "cancelled" and order_record["state"] in data.order_states:
                total = total + order_record["product_price"]
            elif with_cart and order_record["state"] == "cart":
                total = total + order_record["product_price"]

    data.orders[order_id]["total"] = total


def orders_total_price():
    for order in data.orders.values():
        order["total"] = 0.0
    for order_record in data.orders_record.values():
        if(order_record["state"] in data.order_states and order_record["state"] != "cancelled"):
            data.orders[order_record["order_id"]]["total"] = data.orders[order_record["order_id"]
                                                                         ]["total"] + order_record["product_price"]


def table_reset_parameters(table_id):
    data.tables[table_id]["relative_height"] = 50
    data.tables[table_id]["first_heath_section"] = False
    data.tables[table_id]["second_heath_section"] = False
    data.tables[table_id]["third_heath_section"] = False
    data.tables[table_id]["fourth_heath_section"] = False
    data.tables[table_id]["waiter_call"] = False


def new_order(table_id):
    aux = list()

    for order_id in data.orders:
        aux.append(int(order_id))

    new_order_id = str(max(aux) + 1)

    del aux

    data.orders[new_order_id] = dict()
    data.orders[new_order_id]["date_time"] = str(datetime.datetime.now())
    data.orders[new_order_id]["bill_requested"] = False
    data.orders[new_order_id]["pay_by_card"] = False
    data.orders[new_order_id]["paid"] = False
    data.orders[new_order_id]["invoice"] = False
    data.orders[new_order_id]["table_id"] = table_id

    return new_order_id


def get_all_cart_order_records(order_id):
    record_id_list = []

    for order_record_id, order_record in data.orders_record.items():
        if order_record["order_id"] == order_id and order_record["state"] == "cart":
            record_id_list.append(order_record_id)

    return record_id_list


def confirm_cart_order_records(order_id):
    record_id_list = get_all_cart_order_records(order_id)

    for record_id in record_id_list:
        data.orders_record[record_id]["state"] = "pending"


def cancel_cart_order_records(order_id):
    record_id_list = get_all_cart_order_records(order_id)

    for record_id in record_id_list:
        del data.orders_record[record_id]


def new_order_record(order_id, product_id):
    aux = list()

    for order_record_id in data.orders_record:
        aux.append(int(order_record_id))

    new_order_record_id = str(max(aux) + 1)

    del aux

    data.orders_record[new_order_record_id] = dict()
    data.orders_record[new_order_record_id]["order_id"] = order_id
    data.orders_record[new_order_record_id]["product_id"] = product_id
    data.orders_record[new_order_record_id]["product_price"] = data.products[product_id]["price"]
    data.orders_record[new_order_record_id]["state"] = "cart"

    return new_order_record_id


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def tables_count_notifications():
    for table_id, table in data.tables.items():
        count = 0
        order_id = order_get_latest(table_id)
        if table["waiter_call"] or table["waiter_call"] == "":
            count = count + 1
        if order_is_valid(order_id):
            if data.orders[order_id]["bill_requested"]:
                count = count + 1
            for order_record in data.orders_record.values():
                if(order_record["order_id"] == order_id and
                    (order_record["state"] == "pending" or
                        order_record["state"] == "ear_kitchen")):
                    count = count + 1
        table["notifications"] = count


def make_active_product_category(active_category="drinks"):
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
    tables_count_notifications()
    tables_are_occupied()
    return render_template("/tables/list.html", title="Mesas",
                           img_viewer=False, fixed_navbar=True,
                           tables=data.tables, customer=False)


@app.route("/waiter/tables/<num>/info.html", methods=['GET', 'POST'])
def waiter_table(num):
    if num in data.tables:
        if request.method == 'POST':
            if("state" in request.form and "record-id" in request.form
                    and request.form["state"] in data.order_states
                    and request.form["record-id"] in data.orders_record):
                data.orders_record[request.form["record-id"]
                                   ]["state"] = request.form["state"]
            elif("order-id" in request.form and "paid" in request.form
                    and request.form["order-id"] in data.orders):
                data.orders[request.form["order-id"]]["paid"] = True
                table_reset_parameters(
                    data.orders[request.form["order-id"]]["table_id"])
            elif "waiter-completed" in request.form:
                data.tables[num]["waiter_call"] = False
        latest_order_id = order_get_latest(num)
        table_is_occupied(num)
        return render_template("/tables/info.html", title="Mesa "+num,
                               num=num, img_viewer=True, fixed_navbar=True,
                               orders_record=collections.OrderedDict(
                                   reversed(list(data.orders_record.items()))),
                               states=data.order_states, orders=data.orders,
                               tables=data.tables, products=data.products,
                               latest_order_id=latest_order_id,
                               customer=False)
    else:
        abort(404)


@app.route("/waiter/orders/list.html")
def waiter_orders():
    orders_total_price()
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
        if "product-price" in request.form and isfloat(request.form["product-price"]):
            data.products[request.form["product-id"]
                          ]["price"] = float(request.form["product-price"])
        else:
            data.products[request.form["product-id"]
                          ]["available"] = not data.products[request.form["product-id"]
                                                             ]["available"]
        make_active_product_category(request.form["current-category"])
    else:
        make_active_product_category()
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
    if request.method == 'POST' and "table-id" in request.form and request.form["table-id"] in data.tables:
        return redirect("/customer/tables/" + request.form["table-id"] + "/home.html")
    else:
        return render_template("/customer/home.html", title="Cliente",
                               img_viewer=False, fixed_navbar=False,
                               customer=True, tables=data.tables)


@app.route("/customer/tables/<num>/home.html", methods=['GET', 'POST'])
def customer_table(num):
    if num in data.tables:
        latest_order_id = order_get_latest(num)
        table_is_occupied(num)
        if request.method == 'POST':
            if "waiter-call" in request.form:
                data.tables[num]["waiter_call"] = request.form["waiter-call"]
                return redirect("/customer/tables/" + num + "/info.html")
            elif data.tables[num]["occupied"]:
                if("end-order" in request.form and "pay-by-card" in request.form and
                        "invoice" in request.form and not data.orders[latest_order_id]["bill_requested"]
                        and not order_has_pending_record(latest_order_id)):
                    data.orders[latest_order_id]["bill_requested"] = True
                    if request.form["pay-by-card"].lower() == "true":
                        data.orders[latest_order_id]["pay_by_card"] = True
                    if request.form["invoice"].lower() == "true":
                        data.orders[latest_order_id]["invoice"] = True
                    return redirect("/customer/tables/" + num + "/orders/" + latest_order_id + "/summary.html")
            else:
                if "new-order" in request.form:
                    new_order_id = new_order(num)
                    return redirect("/customer/tables/" + num + "/orders/" + new_order_id + "/products/list.html")
        return render_template("/tables/home.html", title="Mesa "+num,
                               img_viewer=False, fixed_navbar=False,
                               customer=True, tables=data.tables,
                               has_pending_record=order_has_pending_record(
                                   latest_order_id),
                               latest_order_id=latest_order_id,
                               orders=data.orders, num=num)
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
    if num in data.tables:
        latest_order_id = order_get_latest(num)
        table_is_occupied(num)
        return render_template("/tables/info.html", title="Mesa "+num,
                               num=num, img_viewer=True, fixed_navbar=True,
                               orders_record=collections.OrderedDict(
                                   reversed(list(data.orders_record.items()))),
                               states=data.order_states, orders=data.orders,
                               tables=data.tables, products=data.products,
                               latest_order_id=latest_order_id,
                               customer=True)
    else:
        abort(404)


@app.route("/customer/tables/<num_table>/orders/<num_order>/products/list.html", methods=['GET', 'POST'])
def customer_products_list(num_table, num_order):
    if(num_table in data.tables and num_order == order_get_latest(num_table) and
            data.orders[num_order]["table_id"] == num_table and not data.orders[num_order]["bill_requested"]):
        if request.method == 'POST':
            if("current-category" in request.form and "product-id" in request.form and
                    request.form["current-category"] in data.product_categories and
                    request.form["product-id"] in data.products and
                    data.products[request.form["product-id"]]["available"]):
                new_order_record(num_order, request.form["product-id"])
                make_active_product_category(request.form["current-category"])
            elif "cancel" in request.form:
                cancel_cart_order_records(num_order)
                if not order_has_record(num_order):
                    del data.orders[num_order]
                return redirect("/customer/tables/" + num_table + "/home.html")
        else:
            make_active_product_category()
        order_total_price(num_order, True)
        return render_template("/products/list.html", title="Carta",
                               img_viewer=True, fixed_navbar=True,
                               num_table=num_table, num_order=num_order,
                               categories=data.product_categories,
                               orders=data.orders, customer=True,
                               products=data.products)
    else:
        abort(404)


@app.route("/customer/tables/<num_table>/orders/<num_order>/products/cart.html", methods=['GET', 'POST'])
def customer_products_cart(num_table, num_order):
    if(num_table in data.tables and num_order == order_get_latest(num_table) and
            data.orders[num_order]["table_id"] == num_table and not data.orders[num_order]["bill_requested"]):
        has_cart_record = order_has_cart_record(num_order)
        if request.method == 'POST':
            if("order-record-id" in request.form and request.form["order-record-id"] in data.orders_record
                    and data.orders_record[request.form["order-record-id"]]["order_id"] == num_order):
                del data.orders_record[request.form["order-record-id"]]
            elif "confirm" in request.form and has_cart_record:
                confirm_cart_order_records(num_order)
                return redirect("/customer/tables/" + num_table + "/home.html")
            elif "cancel" in request.form:
                cancel_cart_order_records(num_order)
                if not order_has_record(num_order):
                    del data.orders[num_order]
                return redirect("/customer/tables/" + num_table + "/home.html")
        order_total_price(num_order, True)
        return render_template("/products/cart.html", title="Carrito",
                               img_viewer=True, fixed_navbar=True,
                               num_table=num_table, num_order=num_order,
                               orders_record=collections.OrderedDict(
                                   reversed(list(data.orders_record.items()))),
                               orders=data.orders, customer=True,
                               has_cart_record=has_cart_record,
                               states=data.order_states,
                               products=data.products)
    else:
        abort(404)


@app.route("/customer/tables/<num_table>/orders/<num_order>/summary.html")
def customer_order_summary(num_table, num_order):
    if num_table in data.tables and num_order == order_get_latest(num_table) and data.orders[num_order]["table_id"] == num_table:
        order_total_price(num_order)
        return render_template("/orders/summary.html", title="Resumen pedido",
                               img_viewer=True, fixed_navbar=True,
                               num_table=num_table, num_order=num_order,
                               orders=data.orders, customer=True,
                               orders_record=data.orders_record,
                               states=data.order_states,
                               products=data.products)
    else:
        abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(data.PORT))
