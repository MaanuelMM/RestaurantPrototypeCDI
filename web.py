#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Authors:      Luis Carles Durá, Jaime García Velázquez, Manuel Martín Malagón, Rafael Rodríguez Sánchez
# Created:      2019/04/10
# Last update:  2019/04/10


from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory
import os

app = Flask(__name__)


@app.route("/")
def base():
    return redirect("/index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/about.html")
def about():
    return "!", 200

@app.route("/waiter")
def waiter():
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
def customer():
    return redirect("/customer/home.html")

@app.route("/customer/home.html")
def customer_home():
    return "!", 200

@app.route("/products/list.html")
def products_list():
    return render_template("/products/list.html")

if __name__ == "__main__":
    app.run(debug=True)